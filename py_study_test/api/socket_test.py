# encoding:utf-8

import socket

"""
Socket是一个在计算机网络中用于数据通信的抽象概念。
一般来说，我们可以通过Socket向网络中的其他设备发送数据，并从其他设备接收数据。
在Python中，socket是一个标准库，提供了在Python中使用Socket进行网络编程的功能。

在Socket编程中，有两种常见的协议：TCP（传输控制协议）和UDP（用户数据报协议）。
TCP是一种面向连接的协议，数据传输前需要建立连接，而UDP则是一种无连接的协议，数据传输不需要建立连接。
"""

# 1. 创建Socket对象。创建Socket对象时，需要指定Socket类型和协议(TCP or UDP)。
# 1.1 创建TCP连接的Socket对象。AF_INET 表示使用IPv4地址。SOCK_STREAM 表示使用TCP协议
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 1.2 创建UDP连接的Socket对象。SOCK_DGRAM表示使用UDP协议。
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
连接到服务器或绑定到本地IP和端口
连接到服务器或绑定到本地IP和端口时，需要指定IP地址和端口号。
对于客户端连接，可以使用connect()方法连接到服务器；
对于服务器，可以使用 bind() 方法绑定到本地IP和端口，并使用 listen() 方法监听客户端连接请求。
"""

# 2.1 连接到服务器
# tcp_socket.connect(('127.0.0.1', 8000))

# 2.2 绑定到本地IP和端口 (用于创建服务器端套接字对象时，绑定服务端端口)
tcp_server_socket.bind(('127.0.0.1', 8000))

# 2.3 监听客户端连接请求 (用于创建服务器端套接字对象时，监听客户端请求)
tcp_server_socket.listen()

# 2.4 接收客户端的连接 accept()
client_socket, client_info = tcp_server_socket.accept()
# 接收客户端发送的消息
recv_data = client_socket.recv(1024)
print('接收到%s的消息%s' % (client_info, recv_data.decode('gb2312')))

# 3. 发送数据
# 3.1 TCP发送数据
tcp_client_socket.send('hello'.encode())
# # 发送HTTP请求
# http_request = 'GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n'
# tcp_socket.send(http_request.encode())

# 3.2 UDP发送数据
# 创建接收信息的地址 sendto()
addr = ('127.0.0.1', 8080)
udp_socket.sendto('world'.encode(), addr)

# 4. 接收数据
# 4.1 TCP接收数据  表示本次接收的最大字节数1024
recv_data = tcp_client_socket.recv(1024)
print('接收到%s的消息是%s' % (recv_data[1], recv_data[0].decode('gb2312')))
print(recv_data.decode())

# 4.2 UDP接收数据
recv_data, address = udp_socket.recvfrom(1024)
print(recv_data.decode())

# 5. 关闭Socket连接。在通信结束后，需要使用 close() 方法关闭Socket连接。
tcp_client_socket.close()
udp_socket.close()

# 6. 设置Socket连接的超时时间。防止连接过程中出现死等情况。settimeout()
# 设置连接超时时间为5秒
# tcp_socket.settimeout(5)

# 7. 获取本地IP地址和端口号 getsockname()
# 获取本地IP地址和端口号
def getsockname_test():
    # 创建TCP连接的Socket对象
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定到本地IP和端口，并监听客户端连接请求
    tcp_socket.bind(('127.0.0.1', 8000))
    tcp_socket.listen()

    # 获取本地IP地址和端口号
    local_ip, local_port = tcp_socket.getsockname()
    print(f'Local IP: {local_ip}, Local Port: {local_port}')

# 8. getpeername() 获取远程IP地址和端口号。
def getpeername_test():
    # 创建TCP连接的Socket对象
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    tcp_socket.connect(('www.baidu.com', 80))

    # 获取远程IP地址和端口号
    remote_ip, remote_port = tcp_socket.getpeername()
    print(f'Remote IP: {remote_ip}, Remote Port: {remote_port}')

# 9. 在Socket连接中，可能会出现各种异常情况，如连接超时、连接被拒绝、数据发送或接收失败等。
# 为了保证程序的健壮性，需要对这些异常情况进行处理。常见的异常包括 socket.error、socket.timeout 等。
def socket_exception_test():
    # 创建TCP连接的Socket对象
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到服务器
        tcp_socket.connect(('127.0.0.1', 8000))

        # 发送数据
        data = 'hello'
        tcp_socket.send(data.encode())

        # 接收数据
        recv_data = tcp_socket.recv(1024)
        print(recv_data.decode())

    except socket.error as e:
        print(f'Socket error: {e}')
    except socket.timeout as e:
        print(f'Socket timeout: {e}')
    finally:
        # 关闭TCP连接
        tcp_socket.close()

"""
10. 发送http请求
频繁进行HTTP请求，建议使用更高级的库，如requests模块，它可以更方便地进行HTTP请求和处理响应，避免手动构造HTTP请求和解析响应的麻烦。
"""
def send_http_request_test(host, port, path):
    # 构建HTTP请求报文
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"

    # 创建TCP套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到服务器
        tcp_socket.connect((host, port))

        # 发送HTTP请求报文
        tcp_socket.sendall(request.encode())

        # 接收服务器的响应
        response = b""
        while True:
            data = tcp_socket.recv(1024)
            if not data:
                break
            response += data

        # 解析并打印服务器响应
        print(response.decode())

    except Exception as e:
        print("发生异常：", e)

    finally:
        # 关闭套接字连接
        tcp_socket.close()