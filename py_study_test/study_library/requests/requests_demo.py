# encoding: utf-8

import requests

"""
requests 是一个非常流行的 Python 库，用于发送 HTTP 请求。它提供了简单而强大的 API，使得与 HTTP 服务的交互变得非常容易。以下是一些 requests 库中常用的 API 和功能的介绍。


"""

ip = "127.0.0.1:"

# 1. GET请求  超时设置(单位秒): timeout=5
# response = requests.get(ip + "/result")
# 1.1. 设置请求头
headers = {'Authorization': 'Bearer YOUR_TOKEN'}
# 1.2. 设置参数
params = {'param1': 'value1', 'param2': 'value2'}
# 1.3. 设置超时设置(单位秒): timeout=5
# response = requests.get('http://example.com/api', headers=headers, params=params, timeout=5)


# 2. POST请求
# 2.1. 使用 data 参数发送表单数据：
data = {'key1': 'value1', 'key2': 'value2'}
# response = requests.post('http://example.com/api', data=data)

# 2.2. 上传文件 使用 files 参数上传文件
files = {'file': open('file.txt', 'rb')}
# response = requests.post('http://example.com/upload', files=files)


# 3. 响应
# 3.1 响应状态码  response.status_code
# if response.status_code == 200:
#     print("请求成功")


# 3.2 获取响应内容  text = response.text

# 3.3. 获取 JSON 格式的响应内容
# json_data = response.json()  # 自动解析为字典

# 3.4. 获取原始字节内容：
# content = response.content

# 3.5. 错误处理  使用 response.raise_for_status 方法检查请求是否成功，发生错误时抛出异常：
# try:
#     response = requests.get('http://example.com/api')
#     response.raise_for_status()  # 如果状态码不是 200，会抛出异常
# except requests.exceptions.RequestException as e:
#     print("请求发生错误:", e)


# 4.  会话管理  使用 Session 对象可以保持某些参数（如 cookies 和 headers）在多个请求之间共享：
# session = requests.Session()
# session.headers.update({'Authorization': 'Bearer YOUR_TOKEN'})
#
# response1 = session.get('http://example.com/api')
# response2 = session.post('http://example.com/api', data={'key': 'value'})


# 5. 代理设置  如果需要使用代理，可以通过 proxies 参数设置：
# proxies = {
#     'http': 'http://proxy.example.com:8080',
#     'https': 'http://proxy.example.com:8080',
# }
# response = requests.get('http://example.com', proxies=proxies)


# 6. SSL 验证  可以通过 verify 参数控制 SSL 证书验证：
# response = requests.get('https://example.com', verify=False)  # 不验证 SSL 证书（不推荐）

# 7. 常见异常 requests 库会抛出多种异常，常见的有：
# 7.1. requests.exceptions.RequestException：所有请求异常的基类。
# 7.2. requests.exceptions.HTTPError：HTTP 错误（如 404、500 等）。
# 7.3. requests.exceptions.ConnectionError：连接错误。
# 7.4. requests.exceptions.Timeout：请求超时。