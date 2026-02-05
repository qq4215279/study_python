# FastAPI 学习项目

这是一个完整的 FastAPI 学习示例项目，展示了 FastAPI 的核心特性和最佳实践。

## 项目结构

```
fastAPI_/
├── requirements.txt          # 项目依赖
├── models.py                # 数据模型和 Pydantic schemas
├── main.py                  # 主应用文件（核心功能）
├── middleware.py            # 中间件和日志配置
├── advanced_examples.py     # 高级特性演示
└── README.md               # 本说明文件
```

## 核心特性演示

### 1. 基础路由和 CRUD 操作
- `GET /` - 根路径欢迎信息
- `GET /health` - 健康检查
- `POST /users` - 创建用户
- `GET /users` - 获取用户列表（支持分页和筛选）
- `GET /users/{user_id}` - 获取单个用户
- `PUT /users/{user_id}` - 更新用户
- `DELETE /users/{user_id}` - 删除用户（需管理员权限）

### 2. 数据验证和序列化
使用 Pydantic 模型进行：
- 请求数据验证
- 响应数据序列化
- 字段约束和正则表达式验证
- 枚举类型支持

### 3. 依赖注入系统
- 自动依赖解析
- 嵌套依赖
- 带参数的依赖工厂
- 安全认证依赖

### 4. 中间件功能
- 请求日志记录
- 安全头设置
- 速率限制
- 请求验证
- 处理时间统计

### 5. 异常处理
- 自定义异常处理器
- 标准化错误响应
- HTTP 异常处理
- 通用异常捕获

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行主应用
```bash
python main.py
```

或者使用 uvicorn 直接运行：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

## API 使用示例

### 创建用户
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "password123",
    "age": 25
  }'
```

### 获取用户列表
```bash
curl "http://localhost:8000/users?page=1&size=10"
```

### 更新用户
```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"age": 26}'
```

## 高级特性演示

运行高级特性演示：
```bash
python advanced_examples.py
```

这将启动第二个服务在端口 8001，展示：
- 表单处理和文件上传
- WebSocket 支持
- 后台任务
- 缓存机制
- 角色权限控制
- 响应模型继承
- 自定义响应类型

## FastAPI 核心优势

### 1. 高性能
- 基于 Starlette 和 Pydantic
- 异步支持
- 比 Flask 快 300% 以上

### 2. 自动生成文档
- Swagger UI 集成
- ReDoc 支持
- 类型提示驱动

### 3. 现代 Python 特性
- 类型提示
- 异步/await
- Pydantic 数据验证

### 4. 易于学习和使用
- 直观的 API 设计
- 丰富的错误信息
- 详尽的文档

## 最佳实践

### 1. 项目结构
- 模型分离
- 依赖注入
- 中间件分层

### 2. 错误处理
- 统一错误格式
- 适当的 HTTP 状态码
- 详细的错误信息

### 3. 安全考虑
- 输入验证
- 速率限制
- 安全响应头
- 认证授权

### 4. 性能优化
- 异步处理
- 缓存策略
- 连接池
- 批量操作

## 学习资源

- [官方文档](https://fastapi.tiangolo.com/)
- [FastAPI 教程](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Starlette 文档](https://www.starlette.io/)

这个项目涵盖了 FastAPI 的主要特性和实际应用场景，是学习和理解 FastAPI 的良好起点。