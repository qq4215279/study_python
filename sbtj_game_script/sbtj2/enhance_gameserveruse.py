# coding:utf-8

import json
import random
import socket
import struct
import threading
import zlib
from StringIO import StringIO
from request_wrapper import *
import request_wrapper

usage_desc = u'''
python sc ip地址 端口号 [命令]
'''


def usage():
    print usage_desc.decode("UTF-8")


class Client:
    def __init__(self, ip, port, compress):
        self.ip = ip
        self.port = port
        self.sock = None
        self.requestId = 1
        self.buf = ""
        self.compress = compress

    '''
    连接客户端
    '''

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    '''
    发送命令
    '''

    def send(self, command, param={}):
        self._checkConn()
        self._send(command, param)

    '''
    发送命令并且立即获得结果
    '''

    def sendAndEcho(self, command, param={}, request_wrapper=None):
        self._checkConn()
        param = request_wrapper.before_call(param)
        print "send: ", command, ", params:", param
        self._send(command, param)
        return self.recv(request_wrapper, False)

    '''
    接收数据
    '''

    def recv(self, requestWrapper, output=False):
        # 读取包头
        if (len(self.buf) < 4):
            data = self.sock.recv(1024)
            self.buf = self.buf + data

        stream = StringIO(self.buf)
        shift = 0
        datalength = 0
        count = 0

        while True:
            c = stream.read(1)
            if c == b'':
                raise EOFError("balabala")
            i = ord(c)
            datalength |= (i & 0x7f) << shift
            shift += 7
            count += 1
            if not i & 0x80:
                break
        le = count
        # 读取内容
        while (len(self.buf) < datalength + count):
            data = self.sock.recv(1024)
            self.buf = self.buf + data

        stream = StringIO(self.buf)
        shift = 0
        commandlength = 0
        s = stream.read(count)
        while True:
            c = stream.read(1)
            if c == b'':
                raise EOFError("balabala")
            i = ord(c)
            commandlength |= (i & 0x7f) << shift
            shift += 7
            count += 1
            if not i & 0x80:
                break
        command = stream.read(commandlength)

        shift = 0
        id = 0
        while True:
            c = stream.read(1)
            if c == b'':
                raise EOFError("balabala")
            i = ord(c)
            id |= (i & 0x7f) << shift
            shift += 7
            count += 1
            if not i & 0x80:
                break

        msg = stream.read(len(self.buf) - count)

        # 分析包的格式
        # 如果服务器端压缩了，需要解压
        if self.compress:
            msg = zlib.decompress(msg)

        # 保留多余读取的包
        self.buf = self.buf[le + datalength:]

        requestWrapper.after_call(msg)
        print "recv;", msg

        # 解析json数据
        jsonObj = json.loads(msg)
        state = jsonObj['state']
        if state == 3:
            # 推送数据
            # return self.recv(requestWrapper, output)
            pass

        return jsonObj

    '''
    检查连接
    '''

    def _checkConn(self):
        if self.sock is None:
            raise Exception("not connect yet")

    '''
    发送请求
    '''

    def _send(self, cmd, param={}):
        data = ""
        index = 1
        for (key, value) in param.iteritems():
            if index > 1:
                data = data + "&"
            data = data + key + "=" + value
            index = index + 1

        # 组织包
        # length = 32 + 4 + len(data)
        requestIdB = self.encodeVarint(self.requestId)
        lrb = len(requestIdB)
        ldb = len(data)
        lcd = len(cmd)
        cmdB = self.encodeVarint(lcd)
        lcmb = len(cmdB)
        lengthT = lcmb + lcd + lrb + ldb
        lengthTB = self.encodeVarint(lengthT)
        # lengthTB = self.encodeVarint(lengthT + len(lengthTB))
        ltb = len(lengthTB)
        s2 = str(ltb) + "s" + str(lcmb) + "s" + str(lcd) + "s" + str(lrb) + "s" + str(ldb) + "s"
        result = struct.pack(s2, lengthTB, cmdB, cmd, requestIdB, data)
        self.sock.send(result)

        # 发包序号 + 1
        self.requestId = self.requestId + 1

        return result

    '''
    强转
    '''

    def _byte(self, b):
        return chr(b)

    '''
    解码
    '''

    def encodeVarint(self, number):
        buf = b''
        while True:
            towrite = number & 0x7f
            number >>= 7
            if number:
                buf += self._byte(towrite | 0x80)
            else:
                buf += self._byte(towrite)
                break
        return buf

    def close(self):
        self.sock.close()
        self.buf = ""


class Task(threading.Thread):

    def __init__(self, name="", password="", ifCreateUser=False, content=Content()):
        threading.Thread.__init__(self)
        self.name = name
        self.password = password
        self.commands = []
        self.ifCreateUser = ifCreateUser
        self.client = Client("10.9.200.117", 8858, False)
        self.client.connect()
        if (self.ifCreateUser):
            # 创建用户
            self.sendAndEcho("user@createUser",
                             {"userName": "%s" % self.name, "password": "%s" % self.password, "yx": "aoshitang"})
        # 用户登录
        self.sendAndEcho("user@login",
                         {"userName": "%s" % self.name, "password": "%s" % self.password, "serverId": "aoshitang",
                          "platform": "PC"})
        if (self.ifCreateUser):
            # 创建角色
            self.sendAndEcho("player@createPlayer", {"playerName": "%s" % self.name, "teamId": "1"})
        # 获取角色列表
        playerId = self.sendAndEcho("player@getPlayerList", {})["data"]["playerList"][0]["playerId"]

        # 获取角色属性
        self.sendAndEcho("player@getPlayerInfo", {"playerId": "%s" % str(playerId)})
        # 选择出生点
        if (self.ifCreateUser):
            self.sendAndEcho("world@selectBirth", {"position": "6"})
        self.content = content

    def addCommand(self, command, params={}, request_wrapper=RequestWrapper):
        self.commands.append((command, params, request_wrapper))

    def run(self):
        for command, params, request_wrapper in self.commands:
            self.sendAndEcho(command, params, request_wrapper)
        self.close()

    def sendAndEcho(self, command, params={}, request_wrapper=None):
        if request_wrapper is None:
            self.request_wrapper = RequestWrapper(None)
        else:
            self.request_wrapper = request_wrapper
        return self.client.sendAndEcho(command, params, self.request_wrapper)

    def close(self):
        try:
            self.client.close()
        except:
            print "close client error!"
            pass
