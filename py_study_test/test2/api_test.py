# encoding: utf-8

import asyncio
import threading
from collections import deque
import websockets
import time
import requests
from google.protobuf import json_format

import helper
# protobuf 协议文件！
from client_pb2 import *

# 配置文件
config_dict = helper.parse_config()
# 协议
protocal = helper.read_protocal(config_dict["client_ts_path"])
# 协议名 与 协议id 字典
name_protocol_id_dict = protocal[0]
#  协议id  与协议名 字典
protocol_id_name_dict = protocal[1]

# 不需要打印的协议
FILTER_PRINT_MESSAGE_SET = {}
# FILTER_PRINT_MESSAGE_SET = {"OnPushFunctionStateListMessage"}


"""
任务
"""
class Task(threading.Thread):
    def __init__(self, playerCount=1, callbackByClose=None):
        threading.Thread.__init__(self)
        self.ws = config_dict["ws"]
        self.env = config_dict["env"]
        # 是否创角
        self.is_create_player = config_dict["is_create_player"]

        self.playerCount = playerCount
        self.callbackByClose = callbackByClose

        self.client_dict = list[Client]
        self.name_alltimes_dict = {}

        self.init = False
        # 初始化客户端
        self.__init_clients()

        # 锁
        self.lock = threading.Lock()
        # 命令
        self.commands = []


    # 初始化客户端
    def __init_clients(self):
        for i in range(self.playerCount):
            try:
                asyncio.run(self.__init_client())
            except RuntimeError as e:
                print("new Client fail i: ", i, e)

        self.init = True

    # do初始化客户端
    async def __init_client(self):
        try:
            deviceId = helper.find_device_id(self.env, self.is_create_player)
            client = Client(self.ws, self.env, deviceId, self.name_alltimes_dict)
            # 建立连接
            await client.connect()
            self.client_dict[deviceId] = client
        except RuntimeError as e:
            print("new Client fail deviceId: ", deviceId, e)


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
                # self.send_msg_and_receive("ReqKeepAlive", [True])
                continue

            t = 0
            # 发送请求
            for protocol_name, params, callback in all_commands:
                # self.send_msg_and_receive(protocol_name, params)
                for client in self.client_dict.values():
                    client.add_command(protocol_name, params, callback)

        else:
            self.task_close()

    """
  添加指令
  """

    def add_command(self, protocol_name: str, params: list, callback=None):
        try:
            self.lock.acquire()
            self.commands.append((protocol_name, params, callback))
        except RuntimeError as e:
            print(e)
        finally:
            self.lock.release()

    """
  发送指令且接受回复
  """

    def send_msg_and_receive(self, protocol_name, params):
        # TODO delete
        pass
        # return self.client.send_msg_and_receive(protocol_name, params)

    """
  关闭连接
  """

    def task_close(self):
        try:
            if not self.callbackByClose is None:
                print("开始关闭连接... name_alltimes_dict: ", self.name_alltimes_dict)
                self.callbackByClose(self.name_alltimes_dict)

            for client in self.client_dict.values():
                asyncio.run(client.client_close())

            # TODO ugly delay!!!
            time.sleep(3)
        except RuntimeError as e:
            print(f"close client error! {e}")
        finally:
            print("task close all clients success!")




"""
客户端
"""
class Client:
    def __init__(self, ws=None, env=None, deviceId=None, name_alltimes_dict={}):
        self.ws = ws
        self.env = env
        # 登录deviceId
        self.deviceId = deviceId

        self.is_running = False

        self.websocket = None
        self.seq = 0
        # 用于存储请求
        self.queue = deque()
        self.send_task = None
        self.receive_task = None

        self.seq_callback_dict = {}

        # TODO 压测记录
        self.name_alltimes_dict = name_alltimes_dict

    """
  建立连接
  """

    async def connect(self):
        """连接到 WebSocket 服务器"""
        self.websocket = await websockets.connect(self.ws)
        self.is_running = True
        print("已连接到 WebSocket 服务器")

        # 初始化
        await self.__init()

        # 启动发送消息的任务
        self.send_task = asyncio.create_task(self.send_messages())
        # 启动接收消息的任务
        self.receive_task = asyncio.create_task(self.receive_messages())

    def is_connect(self):
        if self.websocket is None:
            raise RuntimeError("未连接上服务器！")

    # 初始化
    async def __init(self):
        # 1. 账号服进行游客登录
        token = await self.__account_login()
        print(f"deviceId: {self.deviceId}, token: {token}")

        # 2. 游戏登录
        login_res_msg_arr = await self.__send_msg_and_receive("ReqLoginMessage", {"token": token})
        clientPlayerInfo = login_res_msg_arr[1].clientPlayerInfo

        write_dict = {"isUsed": 1, "deviceId": self.deviceId, "playerId": clientPlayerInfo.id,
                      "nick": clientPlayerInfo.nick}
        helper.add_player_account(self.env, self.deviceId, write_dict)

    # account服登录
    async def __account_login(self):
        data = {'guest': True, 'deviceId': self.deviceId, 'channel': 'dev'}
        response = requests.post(config_dict["login"] + "/account/login", json=data)
        res = response.json()
        if res["code"] != 0:
            raise RuntimeError("登录失败....")

        return res["data"]["token"]

    """
     添加命令
    """
    def add_command(self, protocol_name, params, callback=None):
        encode_send_data = self.__encode_send_param(protocol_name, params)
        # print("addCommand: ", protocol_name, " send_data: ", send_data)

        if callback is not None:
            self.seq_callback_dict[self.seq] = callback
        # 将请求添加到队列
        self.queue.append(encode_send_data)

    """
  发送消息 并接收
  """

    async def __send_msg_and_receive(self, protocol_name, params) -> []:
        await self.__send_msg(protocol_name, params)
        # 处理请求
        return await self.__receive()

    """
  发送消息
  """
    async def __send_msg(self, protocol_name, params):
        """发送请求到 WebSocket 服务器"""
        self.is_connect()

        # TODO 暂时不支持数组！ 将参数的数组类型转为字典类型
        # if isinstance(params, list):
        #   params = self.__convert2dict(protocol_name, params)

        # 发送
        encode_send_data = self.__encode_send_param(protocol_name, params)
        # 接收
        await self.websocket.send(encode_send_data)

    """
  接受消息
  """
    async def __receive(self) -> []:
        self.is_connect()

        messageProxy = None
        # 持续接收来自 WebSocket 服务器的消息
        try:
            response = await self.websocket.recv()
            messageProxy = self.__decode_receive_msg(response)

            # 记录接收时间
            # self.__set_name_alltimes_dict(receive_msg[0], self.__getMilliseconds())

        except websockets.ConnectionClosed:
            print("连接已关闭")

        return messageProxy.resMessage

    """ 
  持续向 WebSocket 服务器发送消息
  """

    async def send_messages(self):
        while not self.is_running:
            await asyncio.sleep(1)
            print("send_messages - 等待连接...")

        times = 0

        while True:
            if len(self.queue) > 0:
                times = 0
                # 从队列中取出请求
                message = self.queue.popleft()
                # print("send_data: ", message)
                # 发送请求
                await self.websocket.send(message)

                # 空
            else:
                times = times + 1
                await asyncio.sleep(1)
                if times > 3:
                    # self.is_running = False
                    print("running over!")
                    break

    """
  持续接收来自 WebSocket 服务器的消息
  """

    async def receive_messages(self):
        while not self.is_running:
            time.sleep(1)
            print("receive_messages - 等待连接...")

        while self.is_running:
            try:
                response = await self.websocket.recv()
                messageProxy = self.__decode_receive_msg(response)

                # TODO 回调 test
                seq = messageProxy.seq
                if seq in self.seq_callback_dict:
                    callback = self.seq_callback_dict[seq](messageProxy.resMessage)
                    # callback(messageProxy.resMessage)

                # 记录接收时间
                # self.__set_name_alltimes_dict(receive_msg[0], self.__getMilliseconds())
            except websockets.ConnectionClosed as e:
                print("连接已关闭")
                # self.is_running = False
                break

    # 获取当前时间的毫秒值
    def __getMilliseconds(self):
        return int(time.time() * 1000)

    """
 延迟关闭 TODO delete
 """

    async def delay_close(self):
        """定期发送心跳消息以保持连接"""
        while self.is_running:
            # 发送心跳消息
            # print("ping...")
            # 每1秒发送一次心跳
            await asyncio.sleep(1)
        else:
            await self.client_close()

    """
  断开连接
  """

    async def client_close(self):
        try:
            if self.is_running:
                print("start close...")
                # 停止接收消息
                self.is_running = False
                # 取消发送任务
                if self.send_task:
                    self.send_task.cancel()
                # 取消接收任务
                if self.receive_task:
                    self.receive_task.cancel()

                # 关闭 WebSocket 连接
                await self.websocket.close()
            print("已关闭 WebSocket 连接")

        except RuntimeError as e:
            print("close client error! {e}", e)
        finally:
            helper.reback_player_account(self.env, self.deviceId)
            print("end close...")

    # 获取发送字节数组
    def __encode_send_param(self, protocol_name="", paramsJ={}):
        # if not protocol_name.startswith("C"):
        #   raise ValueError("请求类型错误！")

        messageOb = self.__create_ob(protocol_name, paramsJ)
        # 使用 getattr() 调用指定名称的方法
        messageObSerializeApi = getattr(messageOb, "SerializeToString")
        messageSerializedData = messageObSerializeApi()
        # print("messageSerializedData: ", messageSerializedData)

        # seq++
        self.seq = self.seq + 1
        cmd = int(name_protocol_id_dict[protocol_name])
        messageProxyDict = {"cmd": cmd, "seq": self.seq, "data": messageSerializedData}
        messageProxyOb = self.__create_ob("MessageProxy", messageProxyDict)
        # 使用 getattr() 调用指定名称的方法
        messageProxySerializeApi = getattr(messageProxyOb, "SerializeToString")
        messageProxySerializeData = messageProxySerializeApi()

        # print("messageProxySerializeData: ", messageProxySerializeData)

        return messageProxySerializeData

    # 解码返回消息
    def __decode_receive_msg(self, serialized_data):
        # 反序列化
        # messageProxy = MessageProxy()
        messageProxy = self.__create_ob("MessageProxy", {})
        messageProxy.ParseFromString(serialized_data)
        # print("decode - messageProxy: ", messageProxy)

        cmd = messageProxy.cmd
        seq = messageProxy.seq
        errorCode = messageProxy.errorCode
        resMessage = None
        protocol_name = ""

        data = messageProxy.data
        if messageProxy.cmd is None or messageProxy.cmd == 0 or data is None:
            return messageProxy, None
        else:
            protocol_name = protocol_id_name_dict[str(messageProxy.cmd)]
            resMessage = self.__create_ob(protocol_name, {})
            resMessage.ParseFromString(data)

        # 将 protobuf 对象转换为 JSON 字符串
        resMessage_json = json_format.MessageToJson(resMessage).replace("\n", "").replace(" ", "")

        if protocol_name not in FILTER_PRINT_MESSAGE_SET:
            print("seq: ", seq, " cmd: ", cmd, " errorCode: ", errorCode, " protocolName: ", protocol_name,
                  " resMessage: ", resMessage_json)

        messageProxy.resMessage = resMessage

        return messageProxy

    # 创建对象
    def __create_ob(self, protocol_name: str, attbute_value_dict):
        class_obj = globals()[protocol_name]
        class_obj = class_obj()

        for key, value in attbute_value_dict.items():
            setattr(class_obj, key, value)

        return class_obj


"""
main
"""


async def main():
    client = Client()
    # 建立连接
    await client.connect()

    # ===============================================================================>
    # 请求玩家个人信息  id: 玩家id
    # client.add_command("CWGetPlayerInfoMessage", {})
    # 请求获取自己赠送礼物记录列表  position: 槽位(从0开始)   count: 总数
    # client.add_command("CWGetPlayerSendGiftListMessage", {"position": 2, "count": 200})
    # 请求获取通用表情列表
    # client.add_command("CWGetCommonEmoteListMessage", {})

    # 请求标记完成新手引导
    def callback(resMsg):
        if 3 > 0:
            print("3333")
    client.add_command("CWMarkFinishGuideMessage", {}, callback)




    # ===============================================================================>
    # 等待一段时间后关闭连接
    await client.delay_close()


if __name__ == '__main__':
    # helper.handle_dirty_players_config_data()
    asyncio.run(main())
