"""
多环境配置示例
演示如何根据不同环境加载不同的配置文件
"""

import os
from dotenv import load_dotenv


def setup_environment():
    """根据环境变量设置对应的配置文件"""
    # 获取当前环境（如果没有设置，默认为 development）
    env = os.getenv('ENVIRONMENT', 'development')
    print(f"当前环境: {env}")
    
    # 根据环境选择配置文件
    env_files = {
        'development': '.env.development',
        'testing': '.env.testing', 
        'production': '.env.production'
    }
    
    env_file = env_files.get(env, '.env.development')
    print(f"使用的配置文件: {env_file}")
    
    # 加载对应环境的配置
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"✓ 成功加载 {env_file}")
    else:
        print(f"⚠ 配置文件 {env_file} 不存在，使用默认 .env")
        load_dotenv()


def get_database_config():
    """获取数据库配置"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '5432')),
        'username': os.getenv('DB_USER', 'admin'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'myapp')
    }


def get_api_config():
    """获取API配置"""
    return {
        'base_url': os.getenv('API_BASE_URL', 'https://api.example.com'),
        'api_key': os.getenv('API_KEY', ''),
        'timeout': int(os.getenv('API_TIMEOUT', '30'))
    }


def main():
    print("=" * 60)
    print("多环境配置管理示例")
    print("=" * 60)
    
    # 设置环境
    setup_environment()
    
    # 获取配置
    db_config = get_database_config()
    api_config = get_api_config()
    
    print("\n数据库配置:")
    for key, value in db_config.items():
        # 隐藏密码信息
        if key == 'password':
            print(f"  {key}: {'*' * len(value) if value else '未设置'}")
        else:
            print(f"  {key}: {value}")
    
    print("\nAPI配置:")
    for key, value in api_config.items():
        # 隐藏API密钥
        if key == 'api_key':
            print(f"  {key}: {'*' * min(8, len(value)) if value else '未设置'}...")
        else:
            print(f"  {key}: {value}")
    
    # 显示其他配置
    print(f"\n应用名称: {os.getenv('APP_NAME', 'Unknown')}")
    print(f"日志级别: {os.getenv('LOG_LEVEL', 'INFO')}")
    print(f"调试模式: {os.getenv('DEBUG', 'False')}")


if __name__ == "__main__":
    main()