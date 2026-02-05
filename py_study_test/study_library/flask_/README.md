# Flask 核心 API 学习指南

本项目展示了 Flask 框架的核心 API 使用方法，包含最常用的功能和最佳实践。

## 项目结构

```
flask_/
├── app.py              # 主应用文件，包含所有核心 API 示例
├── templates/          # HTML 模板目录
│   └── index.html     # 示例模板文件
├── static/            # 静态文件目录
│   ├── style.css      # CSS 样式文件
│   └── flask-logo.png # Flask logo 图片
├── requirements.txt   # 依赖包列表
└── README.md         # 说明文档
```

## 核心 API 功能演示

### 1. 路由系统 (@app.route)
- 基础路由定义
- 带参数路由
- 类型转换路由参数

### 2. HTTP 方法处理
- GET、POST、PUT、DELETE 方法支持
- 方法路由限制

### 3. 请求对象 (request)
- 获取请求方法、URL、头部信息
- 处理表单数据
- 获取查询参数

### 4. 响应处理
- HTML 响应
- JSON 响应
- 自定义响应状态码和头部

### 5. 模板渲染 (render_template)
- Jinja2 模板引擎使用
- 数据传递到模板
- 模板继承和包含

### 6. Session 管理
- 用户会话管理
- 登录状态维护
- flash 消息机制

### 7. 错误处理
- 自定义错误页面
- 404、500 等错误处理

### 8. URL 构建 (url_for)
- 动态 URL 生成
- 反向 URL 构建

### 9. 静态文件服务
- CSS、JS、图片等静态资源
- 文件上传处理

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

3. 访问应用：
打开浏览器访问 `http://localhost:5000`

## 可用路由

- `/` - 首页
- `/hello/<name>` - 带参数的问候页面
- `/user/<int:user_id>` - 用户详情页面
- `/methods` - HTTP 方法测试
- `/request-info` - 请求信息查看
- `/form-example` - 表单处理示例
- `/json-response` - JSON API 响应
- `/custom-response` - 自定义响应示例
- `/template` - 模板渲染示例
- `/login` - 用户登录
- `/dashboard` - 仪表板页面
- `/links` - URL 构建示例
- `/static-example` - 静态文件示例

## 学习建议

1. 从简单的路由开始，逐步理解 Flask 的工作原理
2. 实践每个 API 功能，修改代码观察效果
3. 关注安全性和最佳实践
4. 结合实际项目需求进行扩展

## 注意事项

- 生产环境需要设置 `debug=False`
- 密钥需要保密，不要提交到版本控制
- 表单验证需要更加严格的安全措施
- 错误处理应该更加完善