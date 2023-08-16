# encoding: utf-8

import api_test_helper as helper

import socket
import time
from io import BytesIO
import json
import threading

# 配置文件
config_dict = helper.parse_config()

# 协议
protocal = helper.read_protocal(config_dict["protocal_ip"])
# 协议名 与 协议id 字典
name_protocol_id_dict = protocal[0]
#  协议id  与协议名 字典
protocol_id_name_dict = protocal[1]
# 协议名 与 协议内容 字典
protocol_schemas_dict = protocal[2]




lock = threading.Lock()


def read_player(name):
    need_create_player = True
    dict = {}
    try:
        lock.acquire()

        lines = read_lines(name)
        with open(r"./config/" + name + "players", "w", encoding='utf-8') as file:
            for json_str in lines:
                # 创角
                if len(json_str) <= 0 or json_str.find("\"isUsed\": 1") != -1 or not need_create_player:
                    file.write(json_str)
                else:
                    read_dict = json.loads(json_str)
                    read_dict["isUsed"] = 1

                    file.write(json.dumps(read_dict))

                    need_create_player = False
                    dict = read_dict

                file.write("\n")


    except BaseException as e:

        print(e)
    finally:
        lock.release()
        return need_create_player, dict


def write_player(name, dict={}):
    try:
        lock.acquire()

        lines = read_lines(name)
        with open(r"./config/" + name + "players", "w", encoding='utf-8') as file:
            if len(lines) <= 0:
                file.write(json.dumps(dict))
            else:
                file.writelines(lines)
                file.write(json.dumps(dict))
            file.write("\n")

    except BaseException as e:
        print(e)

    finally:
        lock.release()

def re_write(name, account=""):
    try:
        lock.acquire()

        lines = read_lines(name)
        with open(r"./config/" + name + "players", "w", encoding='utf-8') as file:


            for line in lines:
                if line.find(account) != -1:
                    dict = json.loads(line)
                    dict["isUsed"] = 0

                    file.write(json.dumps(dict))
                else:
                    file.write(line)

                file.write("\n")

    except BaseException as e:

        print(e)
    finally:
        lock.release()


def read_lines(name):
    lines = []
    with open(r"./config/" + name + "players", "r", encoding='utf-8') as file:
        try:
            # lock.acquire()
            lines = file.readlines()
        except BaseException as e:
            print(e)
        finally:
            pass
            # lock.release()
    return lines


class Task(threading.Thread):
    def __init__(self, ip="127.0.0.1", port=9310, name="", is_create_player=False):
        threading.Thread.__init__(self)

        self.ip = ip
        self.port = port
        self.name = name
        # 是否创角
        self.is_create_player = is_create_player
        # 命令
        self.commands = []

        # 连接客户端
        self.client = Client(ip, port)

        res = read_player(self.name)
        need_create_player = res[0]
        dict = res[1]
        # 登录
        if not need_create_player:
            self.account = dict["account"]
            self.password = dict["password"]
            self.client.send_msg_and_receive("ReqLoginAccount", [self.account, self.password, dict["channel"], "1.0.0"])
        else:
            # 注册
            receive_dict = self.client.send_msg_and_receive("ReqRegisterTourist", ["test2", "1.0.0", "test22"])
            write_dict = {"isUsed": 1, "account": receive_dict['account'], "password": receive_dict['password'],
                          "channel": receive_dict['channel']}
            write_player(self.name, write_dict)

            self.account = write_dict["account"]
            self.password = write_dict["password"]
            # 登录
            self.client.send_msg_and_receive("ReqLoginAccount", [self.account, self.password, write_dict["channel"], "1.0.0"])


    def run(self):
        for protocol_name, params in self.commands:
            self.send_msg_and_receive(protocol_name, params)

        self.close()

    def add_command(self, protocol_name: str, params: list):
        self.commands.append((protocol_name, params))

    def send_msg_and_receive(self, protocol_name: str, params: list):
        return self.client.send_msg_and_receive(protocol_name, params)

    def close(self):
        try:
            time.sleep(120)
            self.client.close()
        except:
            print("close client error!")
            pass
        finally:
            re_write(self.name)


"""
客户端
"""


class Client:
    def __init__(self, ip="127.0.0.1", port=9310):
        self.ip = ip
        self.port = port
        self.socket = None

        self.__connect()

        if not self.__is_connect():
            raise BaseException("连接不上服务器！")

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def __is_connect(self):
        return self.socket is not None

    """
    发送消息
    """

    def send_msg(self, protocol_name="", params=[]):
        if not self.__is_connect():
            raise RuntimeError("未连接上服务器！")

        self.socket.send(self.__encode_send_param(protocol_name, params))

    """
    发送消息 并接收
    """

    def send_msg_and_receive(self, protocol_name="", params=[]):
        self.send_msg(protocol_name, params)
        return self.__receive()

    def __receive(self):
        # 读取报文的长度
        buf = self.socket.recv(1024)

        stream = BytesIO(buf)
        stream.seek(0)
        # 1. 总长度
        totalLen = self.__read_int(4, stream) + 4
        # print("totalLen: ", totalLen)

        diff = totalLen - len(buf)
        if diff > 0:
            buf += self.socket.recv(diff)

        return self.__decode_receive_msg(buf)

    def close(self):
        self.socket.close()
        print("与服务器断开连接~")

    """
    获取发送字节数组
    """

    def __encode_send_param(self, protocol_name="", params=[]):
        if not protocol_name.startswith("Req"):
            raise ValueError("请求类型错误！")
        if not protocol_name in protocol_schemas_dict:
            raise ValueError("请求协议不存在！")

        protocol_id = name_protocol_id_dict[protocol_name]
        # print("protocol_id: ", protocol_id)

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
                flag = 1 if param else 0
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
        elif type.endswith("{}"):
            # TODO 完善！ {} 情况 eg: ReqGiveMeItems "type":"int64{}"
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
    def __encode_str_2_bytes(self, str=""):
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
        # print("总长度: ", totalLen, " messageId: ", messageId)

        # 协议名
        protocol_name = ""
        if messageId in protocol_id_name_dict:
            protocol_name = protocol_id_name_dict[messageId]

        schemas = dict()
        if protocol_name in protocol_schemas_dict:
            schemas = protocol_schemas_dict[protocol_name]

        res = self.__do_decode_receive_msg(stream, schemas)

        protocol_name = ": "
        if messageId in protocol_id_name_dict:
            protocol_name = protocol_id_name_dict[messageId] + protocol_name
        print(protocol_name, res)

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

if __name__ == '__main__':
    # 本地
    task = Task(config_dict["ip"], config_dict["port"], config_dict["name"], config_dict["is_create_player"])

    # 刷新配置表  0: 服务器类型 1: 所有服务器; 3: hall; 4: game; 5: player; 6: platform
    task.add_command("ReqRefreshConfigTable", [1, False])
    # task.add_command("ReqRefreshConfigTable", [1, True])

    # 获取功能状态
    # task.add_command("ReqFunctionStatus", [0])


    # 1. 获取战令信息
    # task.add_command("ReqGetPlayerWarOrderInfo", [])
    # 2. 请求领取战令通行证奖励
    # task.add_command("ReqGetWarOrderPassCardReward", [])
    # 3. 请求获取夏日寻访信息
    # task.add_command("ReqGetSummerTourInfo", [])
    # 4. 请求寻访  寻访类型: 1: 阳光海滩; 2: 泳池派对    次数
    # task.add_command("ReqDrawSummerTour", [1, 1])
    # 5. 请求领取寻访额外奖励  寻访类型: 1: 阳光海滩; 2: 泳池派对   序列
    # task.add_command("ReqGetSummerTourExtraReward", [1, 1])
    # 6. 请求获取夏日探宝信息
    # task.add_command("ReqGetSummerTreasureInfo", [])
    # 7. 请求夏日探宝  探宝类型: 1: 免费; 2: 普通; 3: 高级   探宝次数
    # task.add_command("ReqDrawSummerTreasure", [1, 1])
    # 8. 请求领取夏日探宝累计任务奖励  需要累计探宝次数
    # task.add_command("ReqGetTreasureCumulateTaskReward", [4])
    # 9. 请求获取战令任务信息
    # task.add_command("ReqGetWarOrderTaskInfo", [])
    # 10. 请求领取战令任务奖励  任务id: >0: 具体任务; -1: 每日任务可领奖列表; -2: 每周任务可领奖列表; -3: 每期任务可领奖列表
    # task.add_command("ReqGetWarOrderTaskReward", [-1])



    task.start()
