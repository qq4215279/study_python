"""
医疗搜索系统使用示例
"""

from medical_search_system import MedicalHybridSearchSystem


def example_usage():
    """使用示例"""
    import os
    
    print("="*80)
    print("医疗混合搜索系统 - 使用示例")
    print("="*80)
    
    # 检查 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("\n错误: 未设置 DASHSCOPE_API_KEY 环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        print("或通过参数传入: MedicalHybridSearchSystem(..., api_key='your-api-key')")
        return
    
    # 1. 初始化系统
    print("\n[步骤 1] 初始化搜索系统...")
    print("使用模型: 阿里云 text-embedding-v3")
    print("注意：首次运行需要调用 API 构建索引，可能需要几分钟")
    search_system = MedicalHybridSearchSystem(
        "train_zh.json",
        embedding_model_name="text-embedding-v3",
        dimension=1024
    )
    
    # 2. 测试查询
    test_queries = [
        "头痛怎么办",
        "感冒咳嗽怎么治疗",
        "胃痛消化不良",
        "皮肤过敏很痒"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"查询: {query}")
        print('='*80)
        
        # 混合搜索
        print("\n【混合搜索结果】")
        results = search_system.hybrid_search(query, top_k=3)
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"  混合分数: {result['hybrid_score']:.4f}")
            print(f"  向量分数: {result['vector_score']:.4f}")
            print(f"  BM25分数: {result['bm25_score']:.4f}")
            print(f"  问题: {result['instruction']}")
            print(f"  回答: {result['output'][:150]}..." if len(result['output']) > 150 else f"  回答: {result['output']}")
        
        # 对比：仅向量搜索
        print("\n【仅向量搜索结果】")
        vector_results = search_system.search(query, top_k=3, method='vector')
        for i, result in enumerate(vector_results, 1):
            print(f"\n结果 {i} (分数: {result['score']:.4f}):")
            print(f"  问题: {result['instruction']}")
            print(f"  回答: {result['output'][:100]}..." if len(result['output']) > 100 else f"  回答: {result['output']}")
        
        # 对比：仅 BM25 搜索
        print("\n【仅 BM25 搜索结果】")
        bm25_results = search_system.search(query, top_k=3, method='bm25')
        for i, result in enumerate(bm25_results, 1):
            print(f"\n结果 {i} (分数: {result['score']:.4f}):")
            print(f"  问题: {result['instruction']}")
            print(f"  回答: {result['output'][:100]}..." if len(result['output']) > 100 else f"  回答: {result['output']}")


if __name__ == "__main__":
    example_usage()
