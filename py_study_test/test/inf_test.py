# encoding: utf-8

import socket
import time
from io import BytesIO
import json

# 协议名 与 协议id 字典
name_protocol_id_dict = dict()
#  协议id  与协议名 字典
protocol_id_name_dict = dict()
# 协议名 与 协议内容 字典
protocol_schemas_dict = dict()


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

        self.__connect()

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def __is_connect(self):
        return self.socket is not None

    def send_msg(self, protocol_name, params):
        if not self.__is_connect():
            raise RuntimeError("未连接上服务器！")

        self.socket.send(self.__encode_send_param(protocol_name, params))

    def send_msg_and_receive(self, protocol_name, params):
        self.send_msg(protocol_name, params)
        return self.__receive()

    def __receive(self):
        # TODO 读取的长度？
        buf = self.socket.recv(2048)
        return self.__decode_receive_msg(buf)

    def close(self):
        self.socket.close()
        print("与服务器断开连接~")

    """
    获取发送字节数组
    """

    def __encode_send_param(self, protocol_name, params):
        if not protocol_name.startswith("Req"):
            raise ValueError("请求类型错误！")
        if not protocol_name in protocol_schemas_dict:
            raise ValueError("请求协议不存在！")

        protocol_id = name_protocol_id_dict[protocol_name]
        print("protocol_id: ", protocol_id)

        data = b""
        # 协议id
        value = self.__encode_int_2_bytes(4, protocol_id)
        data += value

        i = 0
        for schema in protocol_schemas_dict[protocol_name]:
            type = schema["type"]

            param = params[i] if len(params) > i else None
            i += 1
            data += self.__do_encode_send_param(type, param)

        # 总长度
        totalLen = self.__encode_int_2_bytes(4, len(data))
        return totalLen + data

    # do 获取发送字节数组
    def __do_encode_send_param(self, type, param):
        data = b""
        if type.endswith("[]"):
            type = type[:len(type) - 2]

            # 数组长度
            len = len(param)
            lenB = self.__encode_int_2_bytes(4, len)
            data += lenB

            for i in range(len):
                data += self.__encode_param(type, param)

        else:
            data += self.__encode_param(type, param)

        return data

    # 编码参数
    def __encode_param(self, type, param):
        if type == 'boolean':
            flag = 0
            if isinstance(param, bool):
                flag = 1 if True else 0
            if isinstance(param, str):
                flag = 1 if param.islower() == "true" else 0

            value = self.__encode_int_2_bytes(1, flag)
        if type == 'int8':
            value = self.__encode_int_2_bytes(1, param)
        elif type == 'int16':
            value = self.__encode_int_2_bytes(2, param)
        elif type == 'int32':
            value = self.__encode_int_2_bytes(4, param)
        elif type == 'int64':
            value = self.__encode_int_2_bytes(8, param)
        elif type == 'float':
            value = self.__encode_int_2_bytes(4, param)
        elif type == 'double':
            value = self.__encode_int_2_bytes(8, param)
        elif type == 'string':
            value = self.__encode_str_2_bytes(param)
        elif type.endswith("*"):
            # TODO 完善！ * 情况 eg: "type":"ThirdParty*"
            value = self.__encode_int_2_bytes(1, 0)

        return value

    # 编码 int 类型
    def __encode_int_2_bytes(self, size, num):
        if num is None:
            num = 0

        intB = num.to_bytes(size, "big")
        return intB

    # 编发 字符串类型
    def __encode_str_2_bytes(self, str):
        # 字符串为空
        if str is None or len(str) <= 0:
            return self.__encode_int_2_bytes(4, 0)

        # 字符串
        strB = str.encode(encoding='utf-8')
        # 字符串长度
        lenB = self.__encode_int_2_bytes(4, len(strB))
        return lenB + strB

    """
    解码返回消息
    """

    def __decode_receive_msg(self, buf):
        stream = BytesIO(buf)
        stream.seek(0)

        # 1. 总长度
        totalLen = self.__read_int(4, stream)
        # 2. messageId
        messageId = self.__read_int(4, stream)
        print("总长度: ", totalLen, " messageId: ", messageId)

        # 协议名
        protocol_name = ""
        if messageId in protocol_id_name_dict:
            protocol_name = protocol_id_name_dict[messageId]

        schemas = dict()
        if protocol_name in protocol_schemas_dict:
            schemas = protocol_schemas_dict[protocol_name]

        res = self.__do_decode_receive_msg(stream, schemas)

        print("res: ", res)
        return res

    # 解码返回消息
    def __do_decode_receive_msg(self, stream, schemas):
        res = dict()
        for schema in schemas:
            field = schema['field']
            type = schema['type']

            self.__decode_schemas(res, stream, field, type)

        return res

    # 解码协议
    def __decode_schemas(self, res, stream, field, type):
        # 是可选参数
        if type.endswith("*"):
            type = type[:len(type) - 1]

            flag = True if 1 == self.__read_int(1, stream) else False
            # 传了
            if flag:
                res[field] = self.__do_decode_schema(stream, type)
            else:
                # 赋个默认值！
                if type.endswith("[]"):
                    res[field] = []
                else:
                    res[field] = self.__get_default_value(type)
        else:
            res[field] = self.__do_decode_schema(stream, type)

    # do 解码具体协议
    def __do_decode_schema(self, stream, type):
        # 数组
        if type.endswith("[]"):
            type = type[:len(type) - 2]

            array = []
            arr_size = self.__read_int(4, stream)
            for i in range(arr_size):
                array.append(self.__do_decode_value(stream, type))

            return array
        else:
            return self.__do_decode_value(stream, type)

    # 根据类型 解码值
    def __do_decode_value(self, stream, type):
        if type == 'boolean':
            return True if 1 == self.__read_int(1, stream) else False
        if type == 'int8':
            return self.__read_int(1, stream)
        if type == 'int16':
            return self.__read_int(2, stream)
        if type == 'int32':
            return self.__read_int(4, stream)
        if type == 'int64':
            return self.__read_int(8, stream)
        if type == 'float':
            byte_val = stream.read(4)
            return int.from_bytes(byte_val, "big")
        elif type == 'string':
            return self.__decode_bytes_2_str(stream)
        else:
            schemas = protocol_schemas_dict[type]
            return self.__do_decode_receive_msg(stream, schemas)

    # 获取默认值
    def __get_default_value(self, type):
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
    def __read_int(self, read_size, stream):
        byte_val = stream.read(read_size)
        value = int.from_bytes(byte_val, "big")
        return value

    # 读 string 类型
    def __decode_bytes_2_str(self, stream):
        str_len = self.__read_int(4, stream)
        str_byte = stream.read(str_len)

        if str_byte is None or len(str_byte) <= 0:
            return ""
        return str_byte.decode(encoding='utf-8')


"""
读取协议
"""
def read_protocal():
    # path = r"./"
    path = r"\\10.198.141.130\sgp_dev\\protocalGenSG\liuzhen\\"
    with open(path + "my_protocal_name_to_id.json", "r", encoding='utf-8') as my_protocal_name_to_id:
        global name_protocol_id_dict
        name_protocol_id_dict = json.load(my_protocal_name_to_id)
        global protocol_id_name_dict
        protocol_id_name_dict = dict(zip(name_protocol_id_dict.values(), name_protocol_id_dict.keys()))

    with open(path + "my_protocal_schemas.json", "r", encoding='utf-8') as my_protocol_id_name_dict:
        global protocol_schemas_dict
        protocol_schemas_dict = json.load(my_protocol_id_name_dict)

if __name__ == '__main__':
    read_protocal()

    ip = "127.0.0.1"
    port = 9310
    client = Client(ip, port)

    # 1. 注册
    # client.send_msg_and_receive("ReqRegisterTourist", ["test2", "1.0.0", "te"])

    # {'requestResult': 1, 'errorTips': '', 'account': 'tr10071', 'password': '12345678', 'channel': 'test2', 'playerInfo': {'playerId': 10109, 'accountId': 10109, 'channel': 'test2', 'cellNo': '', 'type': 0, 'certificationStatus': 4294967295, 'nick': '用户10109', 'head': 'head_portrait_01', 'level': 1, 'exp': 0, 'vip': 0, 'vipExp': 0, 'gold': 200000, 'diamond': 0, 'lotteryPoint': 0, 'tickets': 0, 'maxCannonMultiple': 100, 'equipCannonMultiple': 0, 'chargeCumulative': 0, 'createTime': 1691739668893, 'lastLoginTime': 1691739668893, 'lastChargeTime': 0, 'banChatTime': 0, 'onlineTime': 0, 'currentCannonItemId': 7001, 'curBarbetteId': 11001, 'todayOnlineTime': 138, 'buffInfos': [], 'age': 0, 'hasInviter': False}}
    # 1. 登录
    client.send_msg_and_receive("ReqLoginAccount", ["tr10071", "12345678", "test2", "1.0.0"])

    client.send_msg_and_receive("ReqGetPlayerWarOrderInfo", [])

    time.sleep(5)

    client.close()
