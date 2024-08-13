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
                                                 [self.account, self.password, player_dict["channel"], config_dict["version"], 0])
            else:
                # 注册
                self.__register()

    # 注册
    def __register(self):
        receive_dict = self.client.send_msg_and_receive("ReqRegisterTourist", ["test2", config_dict["version"], 0, "test22", 24013002])[0][1]
        write_dict = {"isUsed": 1, "account": receive_dict['account'], "password": receive_dict['password'],
                      "channel": receive_dict['channel'], "playerId": receive_dict['playerInfo']["playerId"]}
        self.playerId = write_dict["playerId"]
        self.account = write_dict["account"]
        self.password = write_dict["password"]
        # 登录
        self.client.send_msg_and_receive("ReqLoginAccount", [self.account, self.password, write_dict["channel"], config_dict["version"], 0])
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
                # 保持心跳
                self.send_msg_and_receive("ReqKeepAlive", [True])
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
    def send_msg_and_receive(self, protocol_name, params):
        return self.client.send_msg_and_receive(protocol_name, params)


    """
    购买月卡商城礼包
    """
    def buy_month_card(self, goodsId: int):
        self.buy_gift("monthcard", goodsId)

    """
    购买礼包商城礼包
    """
    def buy_charge_gift(self, goodsId: int):
        self.buy_gift("chargegift", goodsId)

    """
    购买svip商城礼包
    """
    def buy_svip_card(self, goodsId: int):
        self.buy_gift("svip", goodsId)

    """
    购买金币商城礼包
    """
    def buy_gold_mail(self, goodsId: int):
        self.buy_gift("gold", goodsId)

    """
    购买点券商城礼包
    """
    def buy_stamps_mail(self, goodsId: int):
            # 增加人民币
            self.send_msg_and_receive("ReqGiveMeItems", [{"1004": 10000}, helper.KEY, 0])
            # TODO 不能通过点券方式购买！
            self.buy_gift("stamps", goodsId)


    """
   下单购买礼包
   shop_name: monthcard-月卡商店; chargegift-礼包商店; svip-大会员储值; (gold-金币商店; stamps-点券)
       (gold-金币商店; flashSale-限时抢购商店; diamond-钻石商店; turret-炮塔商店; item-金币商店; gold-金币商店; monthcard-月卡商店; 
              chargegift-礼包商店; stamps-点券; winTreasure-1元夺宝商店; keyGift-幸运返利商店; guideActivity-指南商店; dailyTreasure-每日寻宝商店; 
              seaToken-至尊海神令商店; seckill-限时秒杀; week-周礼包; month-月礼包; bankrupt-破产补助; carnialLuckDraw-嘉年华幸运转盘; purchaseGift-全服抢购; 
              optionalGift-自选礼包; specialGift-特殊礼包; vip-vip专属礼包; svip-大会员储值; carnialLuckDraw-嘉年华幸运转盘; purchaseGift-全服抢购; )
   """
    def buy_gift(self, shop_name: str, goodsId: int):
        # 设备信息
        deviceInfo = """
        {"oaid":"","firstInstallTime":1717638652111,"model":"MI 9","type":"android","package_name":"com.yaoji.yjby.gf",
			"android_id":"c02d858964d1d669","IMEI":"IXiaomi_MI-9","phone_number":"","applicationInfo":{"name":"com.yaoji.GameApplication","targetSdkVersion":30,
			"dataDir":"/data/user/0/com.yaoji.yjby.gf","nativeLibraryDir":"/data/app/com.yaoji.yjby.gf-yZUUarn8sC6S6MpYPQrfxA==/lib/arm"},
			"version_code":24042802,"lastUpdateTime":1717638652111,"is_first_run":true,"version_name":"9.2.1.0","app_name":"hlby3D","brand":"Xiaomi",
			"install_tag":"1720084661","IMSI":"","performance_type":"High","is_support_astc":true}
        """

        receive_dict = self.send_msg_and_receive("ReqStampsBuyGoods", {"shop": shop_name, "goods": goodsId, "fromType": 0, "logFrom": 1,
                                                                     "orderExtraInfo": {"extraInfo":"", "deviceInfo": deviceInfo}})

        if "errorTips" in receive_dict[0][1] and receive_dict[0][1]["errorTips"].find("点券不足") != -1:
            # 增加点券
            self.add_command("ReqGiveMeItems", [{"1015": 10000}, helper.KEY, 0])
            self.add_command("ReqStampsBuyGoods", {"shop": shop_name, "goods": goodsId, "fromType": 0, "logFrom": 1,
                                                   "orderExtraInfo": {"extraInfo":"", "deviceInfo": deviceInfo}})




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
    def send_msg_and_receive(self, protocol_name, params) -> []:
        self.__send_msg(protocol_name, params)
        return self.__receive(protocol_name)

    """
    发送消息
    """
    def __send_msg(self, protocol_name, params):
        if not self.__is_connect():
            raise RuntimeError("未连接上服务器！")

        # 记录发送时间
        self.__set_name_alltimes_dict(protocol_name, self.__getMilliseconds())

        # 将参数的数组类型转为字典类型
        if isinstance(params, list):
            params = self.__convert2dict(protocol_name, params)

        # 发送
        self.socket.send(self.__encode_send_param(protocol_name, params))

    # 转换params为字典
    def __convert2dict(self, protocol_name: str, params: list) -> dict:
        res = {}
        i = 0
        for schema in protocol_schemas_dict[protocol_name]:
            if schema["type"].endswith("*"):
                continue

            field_ = schema["field"]
            res[field_] = params[i]
            i += 1

        return res

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
    def __encode_send_param(self, protocol_name="", paramsJ={}):
        if not protocol_name.startswith("Req"):
            raise ValueError("请求类型错误！")
        if not protocol_name in protocol_schemas_dict:
            raise ValueError("请求协议不存在！")

        protocol_id = name_protocol_id_dict[protocol_name]
        # print("protocol_id: ", protocol_id)

        data = b""
        # 协议id
        data += struct.pack(">i", protocol_id)

        # 拼参数
        data += self.__do_encode_send_param(protocol_name, paramsJ)

        # 总长度
        totalLen = struct.pack(">i", len(data))
        return totalLen + data

    # do 获取发送字节数组
    def __do_encode_send_param(self, protocol_name="", paramsJ={}):
        data = b""

        # 可选协议参数类型
        if protocol_name.endswith("*"):
            protocol_name = protocol_name[:len(protocol_name) - 1]
            # 没有传，则直接填充0
            if protocol_name not in paramsJ:
                # 默认填充
                data += struct.pack(">b", 0)
                return data

        # 解析协议，拼接传入参数
        for schema in protocol_schemas_dict[protocol_name]:
            singleData = b""
            type = schema["type"]
            field = schema["field"]

            # 是否为数组参数
            isArray = False
            # 是否可选参数
            isOption = False

            if type.endswith("[]"):
                type = type[:len(type) - 2]
                isArray = True

            # 可选参数
            elif type.endswith("*"):
                isOption = True


            # XXX[]
            # 数组
            if isArray:
                # 未传参
                if field not in paramsJ:
                    # 不是可选参数
                    if not isOption:
                        raise ValueError("缺少参数!!! type: " + type + " field: " + type)
                    else:
                        # 默认填充0
                        singleData += struct.pack(">b", 0)
                        data += singleData
                        continue

                singleParamsArrJ = paramsJ[field]
                if not isinstance(singleParamsArrJ, list):
                    raise ValueError("不是数组!!!")

                length = len(singleParamsArrJ)
                singleData += struct.pack(">i", length)

                # 解析数组类型参数
                for singleParams in singleParamsArrJ:
                    singleData += self.__do_encode_send_param(type, singleParams)

            else:
                # 未传参
                if field not in paramsJ:
                    # 不是可选参数
                    if not isOption:
                        raise ValueError("缺少参数!!! type: " + type + " field: " + type)
                    else:
                        # 默认填充
                        singleData += struct.pack(">b", 0)
                        data += singleData
                        continue


                subParamsJ = paramsJ[field]

                # 子协议
                tmp_subType = type
                if type.endswith("*"):
                    tmp_subType = type[:len(type) - 1]

                if tmp_subType in protocol_schemas_dict:
                    singleData += self.__do_encode_send_param(type, subParamsJ)

                # 基本数据结构
                else:
                    singleData += self.__encode_param(type, subParamsJ)

            data += singleData

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
    helper.handle_dirty_players_config_data()
    task = Task()

    # 刷新配置表  0: 服务器类型 1: 所有服务器; 3: hall; 4: game; 5: player; 6: platform    True: 测试服重新下载
    # task.add_command("ReqRefreshConfigTable", [1, False])
    # task.add_command("ReqRefreshConfigTable", [1, True])
    # task.add_command("ReqRefreshConfigTable", [5, False])
    # task.add_command("ReqRefreshConfigTable", [5, True])

    # 获取功能状态
    # task.add_command("ReqFunctionStatus", [])

    # 请求给我发放一些道具
    # 人物经验-1006  会员经验-1005  金币-1001  钻石-1002  荣耀战令-3488  神力-3432  灵力-3364
    # 端午战令-3529 端午勋章经验-3538  大肉粽-3533  红豆粽-3534  蛋黄粽-3536   粽叶-3533  糯米-3534  红豆-3535  五花肉-3536  蛋黄-3537
    # 夏日盛典勋章经验-3595 夏日盛典水枪道具: 3587 3588 3589 3590
    # task.send_msg_and_receive("ReqGiveMeItems", [{"1006": 1000000000}, helper.KEY, 0])
    # task.send_msg_and_receive("ReqGiveMeItems", [{"3587": 1000, "3588": 1000, "3589": 1000, "3590": 1000}, helper.KEY, 10027])
    # 古代战舰图纸-3125  现代战舰图纸-3126  功勋值-3596
    # task.send_msg_and_receive("ReqGiveMeItems", [{"3125": 10000, "3126": 10000, "3596": 1000000}, helper.KEY, 10027])

    # 3621-怪兽结晶
    # task.send_msg_and_receive("ReqGiveMeItems", [{"3621": 1300}, helper.KEY, 0])
    # task.send_msg_and_receive("ReqGiveMeItems", [{"3634": 50, "3635": 500}, helper.KEY, 10080])
    # task.send_msg_and_receive("ReqGiveMeItems", [{"3634": 1}, helper.KEY, 10079])



    # task.send_msg_and_receive("ReqGiveMeItems", [{"1001": 10000000000, "1006": 100000000, "6001": 100000000, "6113": 100000000, "4001": 9999}, helper.KEY, 0])
    # task.add_command("ReqOBUnlockCannonLv", [50000000])


    # 太平洋 ================================================>
    # 0. 请求节日活动信息 festivalType = 52
    # task.add_command("ReqFestivalInfo", [52])

    # 1. 太平洋抽奖(末日宝箱) activityId = 214
    # 1.1. 请求太平洋抽奖信息  activityId
    # task.add_command("ReqPacificLotteryInfo", [214])
    # 1.2. 请求领取太平洋抽奖奖励  activityId  type-抽取宝箱类型  num-抽取次数
    # task.add_command("ReqGainPacificLotteryReward", [214, 1, -1])

    # 2. 太平怪物商人 activityId = 215
    # 2.1. 请求获取怪物商人信息  activityId
    # task.add_command("ReqGetMonsterMerchantInfo", [215])
    # 2.2. 请求领取怪物商人通关奖励  activityId
    # task.add_command("ReqGetMonsterMerchantReward", [215])

    # 3. 机甲商城 activityId = 216  54  + 213
    # task.add_command("ReqFestivalShopInfo", [213])
    # task.add_command("ReqFestivalShopInfo", [216])

    # 4. 限时礼包 activityId = 217  55
    # task.add_command("ReqFestivalShopInfo", [217])



    # task.buy_charge_gift(10389)

    task.start()