"""
python-dotenv 实用工具类
提供常用的配置管理功能
"""

import os
from typing import Optional, Union, Dict, Any
from dotenv import load_dotenv


class DotEnvUtils:
    """python-dotenv 实用工具类"""
    
    @staticmethod
    def init_env(env_file: str = ".env", override: bool = False) -> bool:
        """
        初始化环境变量
        
        Args:
            env_file: 环境文件路径
            override: 是否覆盖已存在的变量
            
        Returns:
            bool: 是否成功加载
        """
        try:
            load_dotenv(env_file, override=override)
            return True
        except Exception as e:
            print(f"加载环境文件失败: {e}")
            return False
    
    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        """获取字符串类型的环境变量"""
        return os.getenv(key, default)
    
    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """获取整数类型的环境变量"""
        try:
            return int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def get_float(key: str, default: float = 0.0) -> float:
        """获取浮点数类型的环境变量"""
        try:
            return float(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """获取布尔类型的环境变量"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on', 't', 'y')
    
    @staticmethod
    def get_list(key: str, separator: str = ",", default: list = None) -> list:
        """获取列表类型的环境变量"""
        if default is None:
            default = []
        
        value = os.getenv(key, "")
        if not value:
            return default
        
        return [item.strip() for item in value.split(separator) if item.strip()]
    
    @staticmethod
    def require_vars(*keys: str) -> Dict[str, str]:
        """
        验证必需的环境变量是否存在
        
        Args:
            *keys: 必需的环境变量键名
            
        Returns:
            Dict[str, str]: 环境变量字典
            
        Raises:
            ValueError: 当必需变量缺失时
        """
        missing = []
        result = {}
        
        for key in keys:
            value = os.getenv(key)
            if value is None:
                missing.append(key)
            else:
                result[key] = value
        
        if missing:
            raise ValueError(f"缺少必需的环境变量: {', '.join(missing)}")
        
        return result
    
    @staticmethod
    def get_database_config(prefix: str = "DB_") -> Dict[str, Any]:
        """
        获取数据库配置
        
        Args:
            prefix: 数据库相关变量的前缀
            
        Returns:
            Dict: 数据库配置字典
        """
        return {
            'host': DotEnvUtils.get_str(f"{prefix}HOST", "localhost"),
            'port': DotEnvUtils.get_int(f"{prefix}PORT", 5432),
            'user': DotEnvUtils.get_str(f"{prefix}USER"),
            'password': DotEnvUtils.get_str(f"{prefix}PASSWORD"),
            'database': DotEnvUtils.get_str(f"{prefix}NAME"),
            'ssl': DotEnvUtils.get_bool(f"{prefix}SSL", False)
        }
    
    @staticmethod
    def mask_sensitive_info(config_dict: Dict[str, Any], 
                          sensitive_keys: list = None) -> Dict[str, Any]:
        """
        隐藏敏感信息
        
        Args:
            config_dict: 配置字典
            sensitive_keys: 敏感键名列表
            
        Returns:
            Dict: 处理后的配置字典
        """
        if sensitive_keys is None:
            sensitive_keys = ['password', 'secret', 'key', 'token']
        
        result = config_dict.copy()
        
        for key, value in result.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in sensitive_keys) and value:
                if isinstance(value, str):
                    result[key] = '*' * min(8, len(value))
                else:
                    result[key] = '***'
        
        return result


# 便捷函数
def load_env(env_file: str = ".env", override: bool = False) -> bool:
    """便捷的环境加载函数"""
    return DotEnvUtils.init_env(env_file, override)

def get_config(key: str, 
               default: Any = "", 
               var_type: type = str) -> Any:
    """
    通用配置获取函数
    
    Args:
        key: 配置键名
        default: 默认值
        var_type: 期望的数据类型
        
    Returns:
        转换后的配置值
    """
    if var_type == str:
        return DotEnvUtils.get_str(key, str(default))
    elif var_type == int:
        return DotEnvUtils.get_int(key, default)
    elif var_type == float:
        return DotEnvUtils.get_float(key, default)
    elif var_type == bool:
        return DotEnvUtils.get_bool(key, default)
    else:
        return var_type(os.getenv(key, str(default)))


# 使用示例
if __name__ == "__main__":
    print("DotEnvUtils 工具类使用示例")
    print("=" * 40)
    
    # 初始化环境
    if load_env():
        print("✓ 环境变量加载成功")
    
    # 使用工具类方法
    app_config = {
        'name': DotEnvUtils.get_str('APP_NAME', 'DefaultApp'),
        'debug': DotEnvUtils.get_bool('DEBUG', False),
        'workers': DotEnvUtils.get_int('MAX_WORKERS', 4),
        'timeout': DotEnvUtils.get_float('TIMEOUT_SECONDS', 30.0)
    }
    
    print("\n应用配置:")
    for key, value in app_config.items():
        print(f"  {key}: {value}")
    
    # 获取数据库配置
    db_config = DotEnvUtils.get_database_config()
    print(f"\n数据库配置: {DotEnvUtils.mask_sensitive_info(db_config)}")
    
    # 验证必需变量
    try:
        required_vars = DotEnvUtils.require_vars('APP_NAME', 'DB_HOST')
        print(f"\n必需变量: {required_vars}")
    except ValueError as e:
        print(f"\n✗ {e}")