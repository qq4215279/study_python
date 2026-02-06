# python-dotenv 学习示例

这是一个完整的 python-dotenv 库学习项目，包含了各种使用场景和最佳实践。

## 项目结构

```
dotenv_/
├── requirements.txt          # 依赖包
├── .env                     # 主配置文件
├── .env.development         # 开发环境配置
├── .env.production          # 生产环境配置
├── config_loader.py         # 基础用法演示
├── multi_env_example.py     # 多环境配置示例
├── flask_integration.py     # Flask 集成示例
├── best_practices.py        # 最佳实践示例
└── README.md               # 说明文档
```

## 安装

```bash
pip install python-dotenv
```

或者安装带CLI工具的版本：
```bash
pip install "python-dotenv[cli]"
```

## 使用示例

### 1. 基础用法
```bash
python config_loader.py
```

### 2. 多环境配置
```bash
# 开发环境
ENVIRONMENT=development python multi_env_example.py

# 生产环境  
ENVIRONMENT=production python multi_env_example.py
```

### 3. Flask 集成
```bash
python flask_integration.py
```

### 4. 最佳实践
```bash
python best_practices.py
```

## 核心功能

### 环境变量加载
- `load_dotenv()` - 加载默认 .env 文件
- `load_dotenv('.env.local')` - 加载指定文件
- `load_dotenv(override=True)` - 覆盖已存在变量

### 配置获取
- `os.getenv('KEY')` - 获取环境变量
- `dotenv_values()` - 获取配置字典
- `find_dotenv()` - 查找 .env 文件

## 最佳实践

1. **安全配置**
   - 敏感信息不提交到版本控制
   - 在 .gitignore 中添加 `.env*`
   - 使用配置管理器隐藏敏感信息

2. **环境分离**
   - 为不同环境创建独立配置文件
   - 通过 ENVIRONMENT 变量切换环境
   - 提供合理的默认值

3. **错误处理**
   - 验证必需的配置项
   - 提供清晰的错误信息
   - 使用默认值避免程序崩溃

## 常见应用场景

- Web 应用配置管理
- 数据库连接配置
- API 密钥管理
- 多环境部署
- 第三方服务集成