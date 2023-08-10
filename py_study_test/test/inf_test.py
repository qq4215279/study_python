# encoding: utf-8

import socket
import struct
import time
from io import StringIO
from io import BytesIO


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    """
    建立连接
    """
    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    """
    是否连接成功
    """
    def _is_connect(self):
        return self.socket is None

    """
    发送请求
    """

    def _sendMsg(self, data):
        self.socket.send(get_send_bytes(data))

"""
获取发送字节数组
"""
def get_send_bytes(strList):
    """
    # 游客注册
    protocolId = 82775532
    # 心跳
    # protocolId = 45185077
    # 获取战令信息
    # protocolId = 59573340

    protocolIdB = protocolId.to_bytes(4, "big")
    # data = struct.pack("II", 4, 82775532)

    # 内容
    channelB = b"test2"
    channelBLen = len(channelB)
    channelBBLen = channelBLen.to_bytes(4, "big")

    versionB = b"1.0.0"
    versionBLen = len(versionB)
    versionBBLen = versionBLen.to_bytes(4, "big")

    shebeiB = b"te"
    shebeiBLen = len(shebeiB)
    shebeiBBLen = shebeiBLen.to_bytes(4, "big")

    totalLen = 4 + (4 + channelBLen) + (4 + versionBLen)
    # totalLen = 4 + (4 + channelBLen) + (4 + versionBLen) + (4 + shebeiBLen)
    totalLenB = totalLen.to_bytes(4, "big")

    finalData = totalLenB + protocolIdB + (channelBBLen + channelB) + (versionBBLen + versionB) + (
                shebeiBBLen + shebeiB)
    print("data: ", finalData)

    """

    data = b""
    for i in strList:
        if isinstance(i, bool):
            intB = i.to_bytes(1, "big")
            data = data + intB
        if isinstance(i, int):
            intB = encode_int_2_bytes(i)
            data = data + intB
        if isinstance(i, float):
            intB = encode_int_2_bytes(i)
            data = data + intB
        if isinstance(i, str):
            strB = i.encode(encoding='utf-8')
            lenB = encode_int_2_bytes(len(strB))
            data += lenB + strB

    totalLen = encode_int_2_bytes(len(data))
    return totalLen + data

def encode_int_2_bytes(i):
    intB = i.to_bytes(4, "big")
    return intB

def decode_bytes_2_int(byte_val):
    return int.from_bytes(byte_val, "big")

def decode_bytes_2_str(byte_val):
    if byte_val is None or len(byte_val) <= 0:
        return ""
    return byte_val.decode(encoding='utf-8')

def decode_receves_msg():
    # data2: b'\x00\x00\x00\x1c\x04\xef\r\xec\x00\x00\x00\x05test2\x00\x00\x00\x051.0.0\x00\x00\x00\x02te'
    # 接收到 % s的消息是 % s
    buf = b"\x00\x00\x00\xeb\x05\xd6o\xc4\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x07tr10063\x00\x00\x00\x0812345678\x00\x00\x00\x05test2\x01\x00\x00\x00\x00\x00\x00'u\x00\x00\x00\x00\x00\x00'u\x00\x00\x00\x05test2\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x0b\xe7\x94\xa8\xe6\x88\xb710101\x00\x00\x00\x10head_portrait_01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\r@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x89\xdfG.\xb7\x00\x00\x01\x89\xdfG.\xb7\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1bY\x00\x00*\xf9\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    stream = BytesIO(buf)
    stream.seek(0)

    # 1. 总长度
    b1 = stream.read(4)
    i1 = decode_bytes_2_int(b1)
    print(i1)

    # 2. messageId
    b2 = stream.read(4)
    i2 = decode_bytes_2_int(b2)
    print(i2)

    # 3. requestResult
    b3 = stream.read(4)
    i3 = decode_bytes_2_int(b3)
    print(i3)

    # 3. errorTips
    b41 = stream.read(4)
    i41 = decode_bytes_2_int(b41)
    print(i41)

    b42 = stream.read(i41)
    s1 = decode_bytes_2_str(b42)
    print(s1)

    # 4. account
    b51 = stream.read(4)
    i51 = decode_bytes_2_int(b51)
    print(i51)

    b52 = stream.read(i51)
    s2 = decode_bytes_2_str(b52)
    print(s2)


if __name__ == '__main__':
    decode_receves_msg()

    # try:
    #     tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    #     ip = "127.0.0.1"
    #     port = 9310
    #     tcp_client_socket.connect((ip, port))
    #
    #     # 获取本地IP地址和端口号
    #     local_ip, local_port = tcp_client_socket.getsockname()
    #     print(f'Local IP: {local_ip}, Local Port: {local_port}')
    #
    #     # TCP发送数据
    #
    #     # 游客注册
    #     protocolId = 82775532
    #     # 心跳
    #     # protocolId = 45185077
    #     # 获取战令信息
    #     # protocolId = 59573340
    #
    #     finalData2 = get_send_bytes((82775532, "test2", "1.0.0", "te"))
    #     print("data2: ", finalData2)
    #
    #     if tcp_client_socket is not None:
    #         tcp_client_socket.send(finalData2)
    #
    #
    #     # TCP接收数据 表示本次接收的最大字节数1024
    #     recv_data = tcp_client_socket.recv(1024)
    #     print('接收到%s的消息是%s', recv_data)
    #     # print('接收到%s的消息是%s' % (recv_data[1], recv_data[0].decode('utf-8')))
    #     # print(recv_data.decode())
    #
    #     # 获取远程IP地址和端口号
    #     remote_ip, remote_port = tcp_client_socket.getpeername()
    #     print(f'Remote IP: {remote_ip}, Remote Port: {remote_port}')
    #
    #     time.sleep(10)
    #
    # except socket.error as e:
    #     print(f'Socket error: {e}')
    # except socket.timeout as e:
    #     print(f'Socket timeout: {e}')
    # except Exception as e:
    #     print(f'Socket Exception: {e}')
    # finally:
    #     tcp_client_socket.close()


