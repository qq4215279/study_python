"""
Flask 核心 API 使用示例
展示 Flask 最常用的核心功能和 API
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import os

# 创建 Flask 应用实例
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于 session 加密

# === 1. 路由装饰器 (@app.route) ===
@app.route('/')
def index():
    """首页路由 - 最基础的路由定义"""
    return '<h1>欢迎来到 Flask 核心 API 学习!</h1>'

@app.route('/hello/<name>')
def hello_name(name):
    """带参数的路由"""
    return f'<h1>Hello, {name}!</h1>'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    """带类型转换的路由参数"""
    return f'<h1>用户 ID: {user_id}</h1>'

# === 2. HTTP 方法处理 ===
@app.route('/methods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def http_methods():
    """处理不同的 HTTP 方法"""
    method = request.method
    if method == 'GET':
        return '<h1>这是 GET 请求</h1>'
    elif method == 'POST':
        return '<h1>这是 POST 请求</h1>'
    elif method == 'PUT':
        return '<h1>这是 PUT 请求</h1>'
    elif method == 'DELETE':
        return '<h1>这是 DELETE 请求</h1>'

# === 3. 请求对象 (request) 的使用 ===
@app.route('/request-info')
def request_info():
    """获取请求信息"""
    info = {
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'args': request.args.to_dict(),  # URL 参数
        'remote_addr': request.remote_addr
    }
    return jsonify(info)

@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    """表单处理示例"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        return f'<h1>收到表单数据:</h1><p>用户名: {username}</p><p>邮箱: {email}</p>'
    return '''
    <form method="post">
        <p><input type="text" name="username" placeholder="用户名"></p>
        <p><input type="email" name="email" placeholder="邮箱"></p>
        <p><input type="submit" value="提交"></p>
    </form>
    '''

# === 4. 响应处理 ===
@app.route('/json-response')
def json_response():
    """JSON 响应"""
    data = {
        'message': 'Hello from Flask!',
        'status': 'success',
        'data': [1, 2, 3, 4, 5]
    }
    return jsonify(data)

@app.route('/custom-response')
def custom_response():
    """自定义响应状态码和头部"""
    from flask import make_response
    
    response = make_response('<h1>自定义响应</h1>', 201)
    response.headers['X-Custom-Header'] = 'Custom Value'
    return response

# === 5. 模板渲染 ===
@app.route('/template')
def template_example():
    """模板渲染示例"""
    users = [
        {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com'},
        {'id': 2, 'name': '李四', 'email': 'lisi@example.com'},
        {'id': 3, 'name': '王五', 'email': 'wangwu@example.com'}
    ]
    return render_template('index.html', title='用户列表', users=users)

# === 6. Session 管理 ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录示例"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 简单的身份验证（实际应用中应该更安全）
        if username == 'admin' and password == '123456':
            session['username'] = username
            flash('登录成功!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误!', 'error')
    
    return '''
    <form method="post">
        <h2>用户登录</h2>
        <p><input type="text" name="username" placeholder="用户名" required></p>
        <p><input type="password" name="password" placeholder="密码" required></p>
        <p><input type="submit" value="登录"></p>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    """仪表板页面"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return f'<h1>欢迎, {session["username"]}!</h1><a href="/logout">退出登录</a>'

@app.route('/logout')
def logout():
    """退出登录"""
    session.pop('username', None)
    flash('已退出登录', 'info')
    return redirect(url_for('index'))

# === 7. 错误处理 ===
@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return '<h1>页面未找到 (404)</h1>', 404

@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return '<h1>服务器内部错误 (500)</h1>', 500

# === 8. URL 构建 ===
@app.route('/links')
def show_links():
    """URL 构建示例"""
    links = {
        '首页': url_for('index'),
        '用户详情': url_for('user_profile', user_id=123),
        '带参数页面': url_for('hello_name', name='Flask'),
        '表单页面': url_for('form_example')
    }
    html = '<h1>URL 链接示例</h1><ul>'
    for name, url in links.items():
        html += f'<li><a href="{url}">{name}</a></li>'
    html += '</ul>'
    return html

# === 9. 静态文件服务 ===
@app.route('/static-example')
def static_example():
    """静态文件使用示例"""
    return '''
    <h1>静态文件示例</h1>
    <img src="/static/flask-logo.png" alt="Flask Logo" style="max-width: 200px;">
    <br>
    <a href="/static/style.css">查看 CSS 文件</a>
    '''

if __name__ == '__main__':
    # 创建必要的目录结构
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Flask 应用启动中...")
    print("访问地址: http://localhost:5000")
    print("可用路由:")
    print("- / (首页)")
    print("- /hello/<name> (带参数路由)")
    print("- /user/<int:id> (类型转换路由)")
    print("- /methods (HTTP 方法测试)")
    print("- /request-info (请求信息)")
    print("- /form-example (表单处理)")
    print("- /json-response (JSON 响应)")
    print("- /custom-response (自定义响应)")
    print("- /template (模板渲染)")
    print("- /login (登录)")
    print("- /dashboard (仪表板)")
    print("- /links (URL 构建)")
    print("- /static-example (静态文件)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)