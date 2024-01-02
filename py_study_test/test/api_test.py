# encoding: utf-8

import helper

import socket
import time
from io import BytesIO
import struct
import threading
import queue

# 配置文件
config_dict = helper.parse_config()

# 协议
protocal = helper.read_protocal(config_dict["protocal_addr"])
# 协议名 与 协议id 字典
name_protocol_id_dict = protocal[0]
#  协议id  与协议名 字典
protocol_id_name_dict = protocal[1]
# 协议名 与 协议内容 字典
protocol_schemas_dict = protocal[2]

"""
任务
"""
class Task(threading.Thread):
    def __init__(self, callback=None, callback2=None):
        threading.Thread.__init__(self)
        self.ip = config_dict["ip"]
        self.port = config_dict["port"]
        self.env = config_dict["env"]
        # 是否创角
        self.is_create_player = config_dict["is_create_player"] == 1

        self.callback2 = callback2

        self.name_alltimes_dict = {}
        # 连接客户端
        self.client = Client(self.ip, self.port, self.name_alltimes_dict, callback)
        self.__init()

        # 锁
        self.lock = threading.Lock()
        # 命令
        self.commands = []


    # 初始化
    def __init(self):
        # 注册
        if self.is_create_player:
            self.__register()
        else:
            flag_player_dict = helper.find_player_account(self.env)
            need_create_player = flag_player_dict[0]
            player_dict = flag_player_dict[1]
            # 登录
            if not need_create_player:
                self.playerId = player_dict["playerId"]
                self.account = player_dict["account"]
                self.password = player_dict["password"]
                self.client.send_msg_and_receive("ReqLoginAccount",
                                                 [self.account, self.password, player_dict["channel"], config_dict["version"]])
            else:
                # 注册
                self.__register()

    # 注册
    def __register(self):
        receive_dict = self.client.send_msg_and_receive("ReqRegisterTourist", ["test2", config_dict["version"], "test22"])[0][1]
        write_dict = {"isUsed": 1, "account": receive_dict['account'], "password": receive_dict['password'],
                      "channel": receive_dict['channel'], "playerId": receive_dict['playerInfo']["playerId"]}
        self.playerId = write_dict["playerId"]
        self.account = write_dict["account"]
        self.password = write_dict["password"]
        # 登录
        self.client.send_msg_and_receive("ReqLoginAccount", [self.account, self.password, write_dict["channel"], config_dict["version"]])
        helper.add_player_account(self.env, self.playerId, write_dict)


    def run(self) -> None:
        t = 0
        while True:
            try:
                self.lock.acquire()
                all_commands = self.commands[:]
                self.commands.clear()
            except RuntimeError as e:
                print(e)
            finally:
                self.lock.release()

            if len((all_commands)) <= 0:
                # 超过3s没有任务，断开连接
                if t >= 3:
                    break
                t += 1
                time.sleep(1)
                continue

            t = 0
            # 发送请求
            for protocol_name, params in all_commands:
                self.send_msg_and_receive(protocol_name, params)

        self.close()

    """
    添加指令
    """
    def add_command(self, protocol_name: str, params: list):
        try:
            self.lock.acquire()
            self.commands.append((protocol_name, params))
        except RuntimeError as e:
            print(e)
        finally:
            self.lock.release()

    """
    发送指令且接受回复
    """
    def send_msg_and_receive(self, protocol_name: str, params: list):
        return self.client.send_msg_and_receive(protocol_name, params)

    """
    关闭连接
    """
    def close(self):
        try:
            if not self.callback2 is None:
                print("开始关闭连接... name_alltimes_dict: ", self.name_alltimes_dict)
                self.callback2(self.name_alltimes_dict)

            time.sleep(3)
            self.client.close()
        except RuntimeError as e:

            print(f"close client error! {e}")
            pass
        finally:
            helper.reback_player_account(self.env, self.playerId)


"""
客户端
"""
class Client:
    def __init__(self, ip="127.0.0.1", port=9310, name_alltimes_dict={}, callback=None):
        self.ip = ip
        self.port = port
        self.socket: socket.socket

        self.name_alltimes_dict = name_alltimes_dict
        self.queue = queue.Queue()
        self.callback = callback


        self.__connect()

        if not self.__is_connect():
            raise BaseException("连接不上服务器！")

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def __is_connect(self):
        return self.socket is not None


    """
    发送消息 并接收
    """
    def send_msg_and_receive(self, protocol_name="", params=[]) -> []:
        self.__send_msg(protocol_name, params)
        return self.__receive(protocol_name)

    """
    发送消息
    """
    def __send_msg(self, protocol_name="", params=[]):
        if not self.__is_connect():
            raise RuntimeError("未连接上服务器！")


        # 记录发送时间
        self.__set_name_alltimes_dict(protocol_name, self.__getMilliseconds())

        # 发送
        self.socket.send(self.__encode_send_param(protocol_name, params))

    """
    接受消息
    """
    def __receive(self, send_protocol_name: str) -> []:
        if not self.__is_connect():
            raise RuntimeError("未连接上服务器！")

        # 3s 超时
        self.socket.settimeout(3)

        res = []
        first = True

        while True:
            try:
                # 首次支持阻塞
                if first:
                    first = False
                else:
                    # 后续不支持阻塞
                    self.socket.setblocking(0)

                # 读取报文的长度
                buf = self.socket.recv(8)
                if not buf:
                    return res

                stream = BytesIO(buf)
                stream.seek(0)
                # 1. 总长度
                byte_val = stream.read(4)
                totalLen = struct.unpack(">i", byte_val)[0] + 4
                # print("totalLen: ", totalLen)

                diff = totalLen - len(buf)
                if diff > 0:
                    buf += self.socket.recv(diff)

                receive_msg = self.__decode_receive_msg(buf)
                res.append(receive_msg)

                self.queue.put(receive_msg)

                if not self.callback is None:
                    self.callback(receive_msg[0], receive_msg[1])

                # 记录接收时间
                self.__set_name_alltimes_dict(receive_msg[0], self.__getMilliseconds())

            except socket.timeout as e:
                # print(f'{send_protocol_name} 接口请求超时！: {e}')
                print(f'{send_protocol_name} 接口请求超时！')
                # 记录接收时间 -1: 表示请求失败
                self.__set_name_alltimes_dict(self.__get_receive_protocol_name(send_protocol_name), -1)
                break
            except BlockingIOError as e:  # 如果没有数据了
                # print(f'没有数据接收了~ 退出循环: {e}')
                # print(f'没有数据接收了~ 退出循环')
                self.socket.setblocking(1)
                # 退出循环
                break
        return res

    # 赋值 name_alltimes_dict
    def __set_name_alltimes_dict(self, protocol_name, mill_seconds):
        alltimes = []
        if protocol_name in self.name_alltimes_dict:
            alltimes = self.name_alltimes_dict[protocol_name]
        alltimes.append(mill_seconds)
        self.name_alltimes_dict[protocol_name] = alltimes

    # 获取当前时间的毫秒值
    def __getMilliseconds(self):
        return int(time.time() * 1000)

    # 获取接收协议名称
    def __get_receive_protocol_name(self, send_protocol_name: str):
        return send_protocol_name.replace("q", "s", 1)

    """
    断开连接
    """
    def close(self):
        self.socket.close()
        print("与服务器断开连接~")

    # 获取发送字节数组
    def __encode_send_param(self, protocol_name="", params=[]):
        if not protocol_name.startswith("Req"):
            raise ValueError("请求类型错误！")
        if not protocol_name in protocol_schemas_dict:
            raise ValueError("请求协议不存在！")

        protocol_id = name_protocol_id_dict[protocol_name]
        # print("protocol_id: ", protocol_id)

        data = b""
        # 协议id
        data += struct.pack(">i", protocol_id)

        i = 0
        for schema in protocol_schemas_dict[protocol_name]:
            type = schema["type"]

            param = params[i] if len(params) > i else None
            i += 1
            data += self.__do_encode_send_param(type, param)

        # 总长度
        totalLen = struct.pack(">i", len(data))
        return totalLen + data

    # do 获取发送字节数组
    def __do_encode_send_param(self, type, param):
        data = b""
        if type.endswith("[]"):
            type = type[:len(type) - 2]

            # 数组长度
            len = len(param)
            data += struct.pack(">i", len)

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
            value = struct.pack(">b", flag)
        if type == 'int8':
            value = struct.pack(">b", param)
        elif type == 'int16':
            value = struct.pack(">h", param)
        elif type == 'int32':
            value = struct.pack(">i", param)
        elif type == 'int64':
            value = struct.pack(">q", param)
        elif type == 'float':
            value = struct.pack(">f", param)
        elif type == 'double':
            value = struct.pack(">d", param)
        elif type == 'string':
            value = self.__encode_str_2_bytes(param)
        elif type.endswith("{}"):
            dict_data = b""
            dict_data += struct.pack(">i", len(param))
            param: dict
            for key, value in param.items():
                dict_data += self.__encode_str_2_bytes(key)
                dict_data += struct.pack(">q", value)
            value = dict_data
        elif type.endswith("*"):
            # TODO 完善！ * 情况 eg: "type":"ThirdParty*"
            value = struct.pack(">b", 0)

        return value

    # 编码 字符串类型
    @staticmethod
    def __encode_str_2_bytes(string: str):
        # 字符串为空
        if string is None or len(string) <= 0:
            return struct.pack(">i", 0)

        # 字符串
        strB = string.encode(encoding='utf-8')
        # 字符串长度
        lenB = struct.pack(">i", len(strB))
        return lenB + strB

    # 解码返回消息
    def __decode_receive_msg(self, buf):
        stream = BytesIO(buf)
        stream.seek(0)

        # 1. 总长度
        len_bytes = stream.read(4)
        totalLen = struct.unpack(">i", len_bytes)[0]
        # 2. messageId
        byte_val = stream.read(4)
        messageId = struct.unpack(">i", byte_val)[0]
        # print("总长度: ", totalLen, " messageId: ", messageId)

        # 协议名
        protocol_name = ""
        if messageId in protocol_id_name_dict:
            protocol_name = protocol_id_name_dict[messageId]
        # 协议
        schemas = dict()
        if protocol_name in protocol_schemas_dict:
            schemas = protocol_schemas_dict[protocol_name]

        # do 解码消息
        receive_msg_dict = self.__do_decode_receive_msg(stream, schemas)

        protocol_name = ""
        if messageId in protocol_id_name_dict:
            protocol_name = protocol_id_name_dict[messageId]

        # 不打印的协议集合
        UN_PRINT_PROTOCAL = {"ResKeepAlive"}
        # 打印结果
        if protocol_name not in UN_PRINT_PROTOCAL:
            print(protocol_name + ": ", receive_msg_dict)

        return protocol_name, receive_msg_dict

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

            byte_val = stream.read(1)
            bool_value = struct.unpack(">b", byte_val)[0]

            has_option = 1 == bool_value
            # 传了
            if has_option:
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
        # 二维数组
        if type.endswith("[][]"):
            type = type[:len(type) - 4]

            array = []
            byte_val = stream.read(4)
            arr_size = struct.unpack(">i", byte_val)[0]
            for i in range(arr_size):
                byte2_val = stream.read(4)
                arr2_size = struct.unpack(">i", byte2_val)[0]

                array2 = []
                for j in range(arr2_size):
                    array2.append(self.__do_decode_value(stream, type))
                array.append(array2)

            return array

        # 一维数组
        elif type.endswith("[]"):
            type = type[:len(type) - 2]

            array = []
            byte_val = stream.read(4)
            arr_size = struct.unpack(">i", byte_val)[0]

            for i in range(arr_size):
                array.append(self.__do_decode_value(stream, type))

            return array
        else:
            return self.__do_decode_value(stream, type)

    # 根据类型 解码值
    def __do_decode_value(self, stream, type):
        if type == 'boolean':
            return 1 == struct.unpack(">b", stream.read(1))[0]
        if type == 'int8':
            return struct.unpack(">b", stream.read(1))[0]
        if type == 'int16':
            return struct.unpack(">h", stream.read(2))[0]
        if type == 'int32':
            return struct.unpack(">i", stream.read(4))[0]
        if type == 'int64':
            byte_val = stream.read(8)
            if len(byte_val) == 4:
                return struct.unpack(">i", byte_val)[0]
            return struct.unpack(">q", byte_val)[0]
        if type == 'float':
            return struct.unpack(">f", stream.read(4))[0]
        if type == 'double':
            return struct.unpack(">d", stream.read(8))[0]
        elif type == 'string':
            return self.__decode_bytes_2_str(stream)
        elif type.endswith("{}"):
            dict_data = {}
            length = struct.unpack(">i", stream.read(4))[0]
            for i in range(length):
                key = self.__decode_bytes_2_str(stream)
                subType = type[:len(type) - 2]
                dict_data[key] = self.__do_decode_value(stream, subType)

            return dict_data
        else:
            schemas = protocol_schemas_dict[type]
            return self.__do_decode_receive_msg(stream, schemas)

    # 解码字符串
    def __decode_bytes_2_str(self, stream):
        str_len = struct.unpack(">i", stream.read(4))[0]
        str_byte = stream.read(str_len)

        if str_byte is None or len(str_byte) <= 0:
            return ""
        return str_byte.decode(encoding='utf-8')

    # 获取默认值
    def __get_default_value(self, type):
        if type == 'boolean':
            return False
        elif type == 'int8':
            return 0
        elif type == 'int16':
            return 0
        elif type == 'int32':
            return 0
        elif type == 'int64':
            return 0
        elif type == 'float':
            return 0.0
        elif type == 'double':
            return 0.0
        elif type == 'string':
            return ""
        else:
            return {}


if __name__ == '__main__':
    # 本地
    task = Task()

    # 刷新配置表  0: 服务器类型 1: 所有服务器; 3: hall; 4: game; 5: player; 6: platform    True: 测试服重新下载
    # task.add_command("ReqRefreshConfigTable", [1, False])
    # task.add_command("ReqRefreshConfigTable", [5, False])
    # task.add_command("ReqRefreshConfigTable", [1, True])

    # 获取功能状态  funcId
    task.add_command("ReqFunctionStatus", [0])

    # 请求给我发放一些道具
    # task.send_msg_and_receive("ReqGiveMeItems", [{"6201": 1000000}, helper.KEY, 10447])
    # task.send_msg_and_receive("ReqGiveMeItems", [{"6201": 1}, helper.KEY, 10446])
    # task.send_msg_and_receive("ReqGiveMeItems", [{"6201": 10000000, "14006": 1000}, helper.KEY, 10468])-

    # 1. 获取战令信息
    # task.add_command("ReqGetPlayerWarOrderInfo", [])

    # 渔场玩法 ---------------------------------------------------------------------->
    # 1. 摇钱树信息
    # task.send_msg_and_receive("ReqPrizePoolInfo", [0])

    # 2. 请求获取龙宫献礼信息
    # task.add_command("ReqGetDragonBlessInfo", [])
    # 请求抽取龙宫献礼奖励  times: 献礼次数
    # task.add_command("ReqDrawDragonBlessReward", [1])
    # 请求获取龙宫献礼赐福奖励
    # task.add_command("ReqGetDragonBlessReward", [])

    # 3. 请求获取弹药库信息
    # task.add_command("ReqGetAmmunitionInfo", [""])
    # 请求抽取弹药库奖励  type: 1：普通弹药库，2：豪华弹药库；  times: 次数
    # task.add_command("ReqDrawAmmunitionReward", [1, 10])

    # 4. 请求获取渔场玩法排行榜  type 排行榜类型 1=猎妖 2=炼金    resetType 重置类型 1=日榜 2=周榜
    # task.add_command("ReqGetFisheryPlayRankInfo", [2, 1])

    # 黄金海妖抽奖 ---------------------------------------------------------------------->
    # 设置黄金海妖玩家赏金值
    # task.add_command("ReqFruitConsole", ["SetGoldenFishLottery 550"])
    # 请求获取黄金海妖抽奖信息
    # task.add_command("ReqGetGoldenFishLotteryInfo", [])
    # 请求抽奖黄金海妖
    # task.add_command("ReqDrawGoldenFishLottery", [])

    # 使用道具
    # task.add_command("ReqUseItem", [14006, 1])



    task.start()