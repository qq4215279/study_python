"""
测试医疗搜索系统
"""

from medical_search_system import MedicalHybridSearchSystem
import json


def test_search_system():
    """测试搜索系统"""
    # 检查 API Key
    import os
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 未设置 DASHSCOPE_API_KEY 环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        return
    
    # 初始化系统
    print("正在初始化搜索系统...")
    print("使用模型: 阿里云 text-embedding-v3")
    search_system = MedicalHybridSearchSystem(
        "train_zh.json",
        embedding_model_name="text-embedding-v3",
        dimension=1024
    )
    
    print("\n" + "="*80)
    print("医疗混合搜索系统 - 测试")
    print("="*80)
    
    # 交互式搜索
    while True:
        print("\n" + "-"*80)
        query = input("\n请输入查询问题（输入 'quit' 退出）: ").strip()
        
        if query.lower() in ['quit', 'exit', '退出', 'q']:
            print("再见！")
            break
        
        if not query:
            continue
        
        print("\n选择搜索方法:")
        print("1. 混合搜索 (推荐)")
        print("2. 向量搜索 (语义搜索)")
        print("3. BM25 搜索 (关键词搜索)")
        
        method_choice = input("请选择 (1/2/3，默认1): ").strip() or "1"
        
        method_map = {
            "1": "hybrid",
            "2": "vector",
            "3": "bm25"
        }
        method = method_map.get(method_choice, "hybrid")
        
        top_k = input("返回结果数量 (默认5): ").strip()
        top_k = int(top_k) if top_k.isdigit() else 5
        
        print(f"\n正在搜索: {query}")
        print(f"搜索方法: {method}")
        print("-"*80)
        
        # 执行搜索
        results = search_system.search(query, top_k=top_k, method=method)
        
        if not results:
            print("未找到相关结果")
            continue
        
        # 显示结果
        for i, result in enumerate(results, 1):
            print(f"\n【结果 {i}】")
            if method == 'hybrid':
                print(f"混合分数: {result['hybrid_score']:.4f} "
                      f"(向量: {result['vector_score']:.4f}, "
                      f"BM25: {result['bm25_score']:.4f})")
            else:
                print(f"分数: {result['score']:.4f}")
            
            print(f"问题: {result['instruction']}")
            print(f"回答: {result['output']}")
            print("-"*80)


if __name__ == "__main__":
    test_search_system()
