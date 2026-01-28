"""
医疗混合搜索系统
结合向量搜索（语义搜索）和 BM25 关键词搜索
"""

import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import pickle
import os
import time

try:
    from rank_bm25 import BM25Okapi
    import jieba
    import dashscope
    from http import HTTPStatus
except ImportError:
    print("请先安装依赖: pip install dashscope rank-bm25 jieba")
    raise


class MedicalHybridSearchSystem:
    """医疗混合搜索系统"""
    
    def __init__(self, 
                 data_path: str,
                 embedding_model_name: str = "text-embedding-v3",
                 cache_dir: str = "./cache",
                 api_key: Optional[str] = None,
                 dimension: int = 1024,
                 base_url: str = "https://dashscope.aliyuncs.com/api/v1"):
        """
        初始化搜索系统
        
        Args:
            data_path: JSON 数据文件路径
            embedding_model_name: embedding 模型名称，默认使用 "text-embedding-v3"
            cache_dir: 缓存目录
            api_key: DashScope API Key，如果不提供则从环境变量 DASHSCOPE_API_KEY 读取
            dimension: 向量维度，支持 512/768/1024，默认 1024
            base_url: API 基础 URL，默认使用国内区域
        """
        self.data_path = data_path
        self.embedding_model_name = embedding_model_name
        self.cache_dir = cache_dir
        self.dimension = dimension
        self.base_url = base_url
        
        # 配置 DashScope API
        dashscope.base_http_api_url = base_url
        dashscope.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not dashscope.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量或通过 api_key 参数传入")
        
        # 创建缓存目录
        os.makedirs(cache_dir, exist_ok=True)
        
        # 加载数据
        self.data = self._load_data()
        
        # 构建索引
        self._build_indexes()
    
    def _load_data(self) -> List[Dict]:
        """加载 JSON 数据"""
        print(f"正在加载数据: {self.data_path}")
        data = []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        print(f"已加载 {len(data)} 条数据")
        return data
    
    def _tokenize(self, text: str) -> List[str]:
        """中文分词"""
        return list(jieba.cut(text))
    
    def _encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        使用阿里云 text-embedding-v3 生成向量
        
        Args:
            texts: 文本列表
            
        Returns:
            numpy array of embeddings
        """
        all_embeddings = []
        batch_size = 10  # DashScope API 限制每批最多 10 条
        
        print(f"正在生成 {len(texts)} 条文本的向量 embeddings...")
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            print(f"处理批次 {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size} "
                  f"({i+1}-{min(i+batch_size, len(texts))}/{len(texts)})")
            
            # 调用 DashScope API
            resp = dashscope.TextEmbedding.call(
                model=dashscope.TextEmbedding.Models.text_embedding_v3,
                input=batch_texts,
                dimension=self.dimension,
                output_type="dense"
            )
            
            if resp.status_code == HTTPStatus.OK:
                # 提取 embeddings
                batch_embeddings = [item['embedding'] for item in resp.output['embeddings']]
                all_embeddings.extend(batch_embeddings)
            else:
                raise RuntimeError(f"Embedding API 调用失败: {resp.status_code} {resp.message}")
            
            # 避免请求过快，添加小延迟
            if i + batch_size < len(texts):
                time.sleep(0.1)
        
        return np.array(all_embeddings)
    
    def _build_indexes(self):
        """构建向量索引和 BM25 索引"""
        # 使用模型名称和维度作为缓存文件名的一部分，避免不同配置冲突
        cache_embedding_path = os.path.join(
            self.cache_dir, 
            f"embeddings_{self.embedding_model_name}_dim{self.dimension}.pkl"
        )
        cache_bm25_path = os.path.join(self.cache_dir, "bm25.pkl")
        
        # 检查缓存
        if os.path.exists(cache_embedding_path) and os.path.exists(cache_bm25_path):
            print("从缓存加载索引...")
            with open(cache_embedding_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            with open(cache_bm25_path, 'rb') as f:
                self.bm25 = pickle.load(f)
            print("索引加载完成")
            return
        
        print("正在构建索引...")
        
        # 准备文本数据
        texts = []
        tokenized_texts = []
        
        for item in self.data:
            # 组合 instruction 和 output 作为搜索文本
            text = item['instruction']
            if item.get('output'):
                text += " " + item['output']
            texts.append(text)
            tokenized_texts.append(self._tokenize(text))
        
        # 构建向量索引
        self.embeddings = self._encode_texts(texts)
        
        # 构建 BM25 索引
        print("正在构建 BM25 索引...")
        self.bm25 = BM25Okapi(tokenized_texts)
        
        # 保存缓存
        print("正在保存索引到缓存...")
        with open(cache_embedding_path, 'wb') as f:
            pickle.dump(self.embeddings, f)
        with open(cache_bm25_path, 'wb') as f:
            pickle.dump(self.bm25, f)
        
        print("索引构建完成")
    
    def vector_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        向量搜索（语义搜索）
        
        Args:
            query: 查询文本
            top_k: 返回前 k 个结果
            
        Returns:
            List of (index, score) tuples
        """
        # 生成查询向量
        query_embeddings = self._encode_texts([query])
        query_embedding = query_embeddings[0]
        
        # 计算余弦相似度
        scores = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # 获取 top_k 结果
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def bm25_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        BM25 关键词搜索
        
        Args:
            query: 查询文本
            top_k: 返回前 k 个结果
            
        Returns:
            List of (index, score) tuples
        """
        # 分词
        tokenized_query = self._tokenize(query)
        
        # BM25 搜索
        scores = self.bm25.get_scores(tokenized_query)
        
        # 获取 top_k 结果
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def hybrid_search(self, 
                     query: str, 
                     top_k: int = 10,
                     vector_weight: float = 0.7,
                     bm25_weight: float = 0.3) -> List[Dict]:
        """
        混合搜索：结合向量搜索和 BM25 搜索
        
        Args:
            query: 查询文本
            top_k: 返回前 k 个结果
            vector_weight: 向量搜索权重
            bm25_weight: BM25 搜索权重
            
        Returns:
            List of result dictionaries
        """
        # 执行两种搜索
        vector_results = self.vector_search(query, top_k=top_k * 2)
        bm25_results = self.bm25_search(query, top_k=top_k * 2)
        
        # 归一化分数到 [0, 1] 区间
        if vector_results:
            max_vector_score = max(score for _, score in vector_results)
            min_vector_score = min(score for _, score in vector_results)
            vector_range = max_vector_score - min_vector_score if max_vector_score != min_vector_score else 1
        else:
            vector_range = 1
        
        if bm25_results:
            max_bm25_score = max(score for _, score in bm25_results)
            min_bm25_score = min(score for _, score in bm25_results)
            bm25_range = max_bm25_score - min_bm25_score if max_bm25_score != min_bm25_score else 1
        else:
            bm25_range = 1
        
        # 合并结果并计算混合分数
        combined_scores = {}
        
        for idx, score in vector_results:
            normalized_score = (score - min_vector_score) / vector_range if vector_range > 0 else 0
            if idx not in combined_scores:
                combined_scores[idx] = {'vector_score': 0, 'bm25_score': 0}
            combined_scores[idx]['vector_score'] = normalized_score
        
        for idx, score in bm25_results:
            normalized_score = (score - min_bm25_score) / bm25_range if bm25_range > 0 else 0
            if idx not in combined_scores:
                combined_scores[idx] = {'vector_score': 0, 'bm25_score': 0}
            combined_scores[idx]['bm25_score'] = normalized_score
        
        # 计算混合分数
        hybrid_results = []
        for idx, scores in combined_scores.items():
            hybrid_score = (vector_weight * scores['vector_score'] + 
                          bm25_weight * scores['bm25_score'])
            hybrid_results.append({
                'index': idx,
                'hybrid_score': hybrid_score,
                'vector_score': scores['vector_score'],
                'bm25_score': scores['bm25_score']
            })
        
        # 按混合分数排序
        hybrid_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        # 返回 top_k 结果
        results = []
        for item in hybrid_results[:top_k]:
            idx = item['index']
            data_item = self.data[idx]
            results.append({
                'instruction': data_item['instruction'],
                'output': data_item.get('output', ''),
                'hybrid_score': item['hybrid_score'],
                'vector_score': item['vector_score'],
                'bm25_score': item['bm25_score']
            })
        
        return results
    
    def search(self, query: str, top_k: int = 10, method: str = 'hybrid') -> List[Dict]:
        """
        统一的搜索接口
        
        Args:
            query: 查询文本
            top_k: 返回前 k 个结果
            method: 搜索方法 ('vector', 'bm25', 'hybrid')
            
        Returns:
            List of result dictionaries
        """
        if method == 'vector':
            results = self.vector_search(query, top_k)
            return [{
                'instruction': self.data[idx]['instruction'],
                'output': self.data[idx].get('output', ''),
                'score': score
            } for idx, score in results]
        
        elif method == 'bm25':
            results = self.bm25_search(query, top_k)
            return [{
                'instruction': self.data[idx]['instruction'],
                'output': self.data[idx].get('output', ''),
                'score': score
            } for idx, score in results]
        
        elif method == 'hybrid':
            return self.hybrid_search(query, top_k)
        
        else:
            raise ValueError(f"Unknown search method: {method}")


def main():
    """主函数：演示搜索系统"""
    # 初始化系统（使用阿里云 text-embedding-v3）
    data_path = "train_zh.json"
    
    # 检查 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("警告: 未设置 DASHSCOPE_API_KEY 环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        print("或通过参数传入: MedicalHybridSearchSystem(..., api_key='your-api-key')")
        return
    
    search_system = MedicalHybridSearchSystem(
        data_path,
        embedding_model_name="text-embedding-v3",
        dimension=1024
    )
    
    print("\n" + "="*60)
    print("医疗混合搜索系统 (使用阿里云 text-embedding-v3)")
    print("="*60)
    
    # 示例查询
    test_queries = [
        "头痛怎么办",
        "感冒咳嗽",
        "胃痛消化不良",
        "皮肤过敏"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        print("-" * 60)
        
        # 混合搜索
        results = search_system.search(query, top_k=3, method='hybrid')
        
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i} (混合分数: {result['hybrid_score']:.4f}):")
            print(f"  问题: {result['instruction']}")
            print(f"  回答: {result['output'][:100]}..." if len(result['output']) > 100 else f"  回答: {result['output']}")
            print(f"  向量分数: {result['vector_score']:.4f}, BM25分数: {result['bm25_score']:.4f}")


if __name__ == "__main__":
    main()
