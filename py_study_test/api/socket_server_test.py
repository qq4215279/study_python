# encoding: utf-8

import socketserver

"""
SocketServer 用于创建TCP服务器。可以理解为是对底层 socket 模块的高级封装！

socketserver是Python标准库中的一个模块，它提供了用于编写网络服务器的框架。
使用socketserver模块，你可以更容易地创建TCP或UDP服务器，处理客户端连接，并与客户端进行数据交互，而无需直接操作底层的套接字。

socketserver模块基于socket模块构建，它提供了一组基础类，可以轻松地创建不同类型的服务器。socketserver模块的主要类包括：

socketserver.TCPServer：用于创建TCP服务器。
socketserver.UDPServer：用于创建UDP服务器。
socketserver.BaseRequestHandler：用于处理请求的基础处理器类，你可以继承它并实现handle()方法来处理客户端请求。
socketserver.StreamRequestHandler：继承自BaseRequestHandler，用于处理基于流式套接字的TCP服务器。
socketserver.DatagramRequestHandler：继承自BaseRequestHandler，用于处理UDP服务器。
使用socketserver模块的一般步骤如下：

定义一个继承自BaseRequestHandler的处理器类，并实现handle()方法来处理客户端请求。

创建一个服务器类，继承自TCPServer或UDPServer，并指定处理器类。

创建服务器对象，并调用serve_forever()方法来启动服务器，它会一直运行并监听客户端连接。
"""

# socketserver.