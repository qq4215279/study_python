# encoding: utf-8

import socket
import struct
import time
from io import StringIO
from io import BytesIO
import json

# 协议名 与 协议id 字典
name_protocol_id_dict = dict()
#  协议id  与协议名 字典
protocol_id_name_dict = dict()
# 协议名 与 协议内容 字典
protocol_schemas_dict = dict()

"""
读取协议
"""


def read_protocal():
    with open(r"./my_protocal_name_to_id.json", "r", encoding='utf-8') as my_protocal_name_to_id:
        global name_protocol_id_dict
        name_protocol_id_dict = json.load(my_protocal_name_to_id)
        global protocol_id_name_dict
        protocol_id_name_dict = dict(zip(name_protocol_id_dict.values(), name_protocol_id_dict.keys()))

    with open(r"./my_protocal_schemas.json", "r", encoding='utf-8') as my_protocol_id_name_dict:
        global protocol_schemas_dict
        protocol_schemas_dict = json.load(my_protocol_id_name_dict)


"""
客户端
"""


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

        # 获取本地IP地址和端口号
        local_ip, local_port = self.socket.getsockname()
        print(f'Local IP: {local_ip}, Local Port: {local_port}')

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def _is_connect(self):
        return self.socket is None

    def _sendMsg(self, protocol_name, params):
        self.socket.send(encode_send_param(protocol_name, params))

    def _sendMsgAndReceive(self, protocol_name, params):
        self.socket.send(encode_send_param(protocol_name, params))

        buf = self.socket.recv(2048)
        return decode_receive_msg(buf)

    def _receive(self):
        buf = self.socket.recv(2048)
        return decode_receive_msg(buf)

    def _close(self):
        self.socket.close()
        print("与服务器断开连接~")


"""
获取发送字节数组
"""


def encode_send_param(protocol_name, params):
    if not protocol_name.startswith("Req"):
        raise ValueError("请求类型错误！")
    if not protocol_name in protocol_schemas_dict:
        raise ValueError("请求协议不存在！")

    protocol_id = name_protocol_id_dict[protocol_name]
    print("protocol_id: ", protocol_id)

    data = b""
    # 协议id
    value = encode_int_2_bytes(4, protocol_id)
    data += value

    i = 0
    for schema in protocol_schemas_dict[protocol_name]:
        type = schema["type"]
        param = params[i]
        i += 1
        data += do_encode_send_param(type, param)

    # 总长度
    totalLen = encode_int_2_bytes(4, len(data))
    return totalLen + data


# do 获取发送字节数组
def do_encode_send_param(type, param):
    data = b""
    if type.endswith("[]"):
        type = type[:len(type) - 2]

        # 数组长度
        len = len(param)
        lenB = encode_int_2_bytes(4, len)
        data += lenB

        for i in range(len):
            data += encode_param(type, param)

    else:
        data += encode_param(type, param)

    return data


# 编码参数
def encode_param(type, param):
    if type == 'boolean':
        flag = 0
        if isinstance(param, bool):
            flag = 1 if True else 0
        if isinstance(param, str):
            flag = 1 if param.islower() == "true" else 0

        value = encode_int_2_bytes(1, flag)
    if type == 'int8':
        value = encode_int_2_bytes(1, param)
    elif type == 'int16':
        value = encode_int_2_bytes(2, param)
    elif type == 'int32':
        value = encode_int_2_bytes(4, param)
    elif type == 'int64':
        value = encode_int_2_bytes(8, param)
    elif type == 'float':
        value = encode_int_2_bytes(4, param)
    elif type == 'double':
        value = encode_int_2_bytes(8, param)
    elif type == 'string':
        value = encode_str_2_bytes(param)
    return value


# 编码 int 类型
def encode_int_2_bytes(size, num):
    if num is None:
        num = 0

    intB = num.to_bytes(size, "big")
    return intB


# 编发 字符串类型
def encode_str_2_bytes(str):
    # 字符串为空
    if str is None or len(str) <= 0:
        return encode_int_2_bytes(0)

    # 字符串
    strB = str.encode(encoding='utf-8')
    # 字符串长度
    lenB = encode_int_2_bytes(4, len(strB))
    return lenB + strB


"""
解码返回消息
"""


def decode_receive_msg(buf):
    stream = BytesIO(buf)
    stream.seek(0)

    # 1. 总长度
    totalLen = read_int(4, stream)
    # 2. messageId
    messageId = read_int(4, stream)
    print("总长度: ", totalLen, " messageId: ", messageId)

    # 协议名
    protocol_name = ""
    if messageId in protocol_id_name_dict:
        protocol_name = protocol_id_name_dict[messageId]

    schemas = dict()
    if protocol_name in protocol_schemas_dict:
        schemas = protocol_schemas_dict[protocol_name]

    res = do_decode_receive_msg(stream, schemas)

    print("res: ", res)
    return res


# 解码返回消息
def do_decode_receive_msg(stream, schemas):
    res = dict()
    for schema in schemas:
        field = schema['field']
        type = schema['type']

        decode_schemas(res, stream, field, type)

    return res


# 解码协议
def decode_schemas(res, stream, field, type):
    # 是可选参数
    if type.endswith("*"):
        type = type[:len(type) - 1]

        flag = True if 1 == read_int(1, stream) else False
        # 传了
        if flag:
            res[field] = do_decode_schema(stream, type)
        else:
            # 赋个默认值！
            if type.endswith("[]"):
                res[field] = []
            else:
                res[field] = get_default_value(type)
    else:
        res[field] = do_decode_schema(stream, type)


# do 解码具体协议
def do_decode_schema(stream, type):
    # 数组
    if type.endswith("[]"):
        type = type[:len(type) - 2]

        array = []
        arr_size = read_int(4, stream)
        for i in range(arr_size):
            array.append(do_decode_value(stream, type))

        return array
    else:
        return do_decode_value(stream, type)


# 根据类型 解码值
def do_decode_value(stream, type):
    if type == 'boolean':
        return True if 1 == read_int(1, stream) else False
    if type == 'int8':
        return read_int(1, stream)
    if type == 'int16':
        return read_int(2, stream)
    if type == 'int32':
        return read_int(4, stream)
    if type == 'int64':
        return read_int(8, stream)
    if type == 'float':
        byte_val = stream.read(4)
        return int.from_bytes(byte_val, "big")
    elif type == 'string':
        return decode_bytes_2_str(stream)
    else:
        schemas = protocol_schemas_dict[type]
        return do_decode_receive_msg(stream, schemas)


# 获取默认值
def get_default_value(type):
    if type == 'boolean':
        return False
    if type == 'int8':
        return 0
    if type == 'int16':
        return 0
    if type == 'int32':
        return 0
    if type == 'int64':
        return 0
    if type == 'float':
        return 0
    elif type == 'string':
        return ""
    else:
        return dict()


# 读 int 类型
def read_int(read_size, stream):
    byte_val = stream.read(read_size)
    value = int.from_bytes(byte_val, "big")
    return value


# 读 string 类型
def decode_bytes_2_str(stream):
    str_len = read_int(4, stream)
    str_byte = stream.read(str_len)

    if str_byte is None or len(str_byte) <= 0:
        return ""
    return str_byte.decode(encoding='utf-8')


if __name__ == '__main__':
    read_protocal()

    ip = "127.0.0.1"
    port = 9310
    client = Client(ip, port)

    name = "ReqRegisterTourist"
    params = ["test2", "1.0.0", "te"]
    client._sendMsgAndReceive(name, params)

    time.sleep(5)

    client._close()
