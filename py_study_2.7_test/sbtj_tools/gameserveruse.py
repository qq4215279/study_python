#coding:utf-8
import json
import random
import socket
import struct
import threading
import zlib
from io import StringIO

from pip._vendor.distlib.compat import raw_input

usage_desc = u'''
python sc ip地址 端口号 [命令]
'''

def usage():
    print(usage_desc.decode("UTF-8"))


class Client():
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
    def sendAndEcho(self, command, param={}, output=False):
        self._checkConn()
        self._send(command, param)
        return self.recv(output)

    def sendJsonAndEcho(self, command, jsonData = "", output=False):
        self._checkConn()
        self._sendJson(command, jsonData)
        return self.recv(output)
        
    def recv(self, output=False):

        # 读取包头
        if(len(self.buf) < 4):
            data = self.sock.recv(1024)
            self.buf = self.buf + data
        
        # 获取长度
        # length = struct.unpack(">i",self.buf[0:4] )
        # length = int(length[0])
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
        while(len(self.buf) < datalength + count):
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
        
        print("recv;", msg)
        print("")

        # 解析json数据
        jsonObj = json.loads(msg)
        state = jsonObj['state']
        if state == 3:
            # 推送数据
            return self.recv(output)
        
        return jsonObj

        
    def _checkConn(self):
        if self.sock is None:
            raise Exception("not connect yet")

    def _send(self, cmd, param={}):
        data = ""
        index = 1
        # for (key, value) in param.iteritems():
        for (key, value) in param.items():
            if index > 1:
                data = data + "&"
            data = data + key + "=" + value
            index = index + 1
        
        # 组织包
        # length = 32 + 4 + len(data)

        # 1. requestId  字节长度
        requestIdB = self.encodeVarint(self.requestId)
        lrb = len(requestIdB)

        # 2. data  长度
        ldb = len(data)

        # 3. cmd 长度
        lcd = len(cmd)

        # 4. cmd 字节长度
        cmdB = self.encodeVarint(lcd)
        lcmb = len(cmdB)

        # 总长度
        lengthT = lrb + ldb + lcd + lcmb
        # 总长度字节表示
        lengthTB = self.encodeVarint(lengthT)
        # lengthTB = self.encodeVarint(lengthT + len(lengthTB))
        # 总长度字节长度
        ltb = len(lengthTB)

        s2 = str(ltb) + "s" + str(lcmb) + "s" + str(lcd) + "s" + str(lrb) + "s" + str(ldb) + "s"
        result = struct.pack(s2, lengthTB, cmdB, cmd, requestIdB, data)

        self.sock.send(result)
        
        # 发包序号 + 1
        self.requestId = self.requestId + 1
        
        return result


    def _byte(self, b):
        return chr(b)

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

    def _sendJson(self, cmd, jsonData = ""):
        # 组织包
        length = 32 + 4 + len(jsonData)
        result = struct.pack(">i32si%ss"%(len(jsonData)), length, cmd, self.requestId, jsonData)
        # 发包
        self.sock.send(result)

        # 发包序号 + 1
        self.requestId = self.requestId + 1

        return result

    def close(self):
        self.sock.close()
        self.buf = ""


name_str = ['a' 'u' 'c' 'b' 'z' 'd' 'e' 'f']

def getRandomName(length=5):
    str = ""
    for i in range(0, length):
        str = str + name_str[random.randint(0, len(name_str) - 1)]
    
    return str

firstP = None

class Task(threading.Thread):
    def __init__(self, name = "", password = "", hasInput = False, ifCreateUser = False):
        threading.Thread.__init__(self)
        self.name = name
        self.password = password
        self.commands = []
        self.jsonCommands = []
        self.hasInput = hasInput
        self.ifCreateUser = ifCreateUser
        # self.client = Client("10.9.200.103", 8858, False)
        self.client = Client("localhost", 8859, False)
        self.client.connect()
        if (self.ifCreateUser):
            # 创建用户
            self.sendAndEcho("user@createUser", {"userName":"%s"%self.name, "password":"%s"%self.password, "yx":"aoshitang"})
        #用户登录
        self.sendAndEcho("user@login", {"userName":"%s"%self.name,"password":"%s"%self.password,"serverId":"aoshitang","platform":"PC"})
        if (self.ifCreateUser):
            # 创建角色
            self.sendAndEcho("player@createPlayer", {"playerName":"%s"%self.name, "teamId":"1"})
        # 获取角色列表
        playerId = self.sendAndEcho("player@getPlayerList",{})["data"]["playerList"][0]["playerId"]

        # 获取角色属性
        self.sendAndEcho("player@getPlayerInfo", {"playerId":"%s"%str(playerId)})

    def addCommand(self, command, params = {}):
        self.commands.append((command, params))

    def addJsonCommand(self, command, jsonData = ""):
        self.jsonCommands.append((command, jsonData))

    def run(self):
        for command, jsonStr in self.jsonCommands:
            self.sendJsonAndEcho(command, jsonStr)

        for command, params in self.commands:
            self.sendAndEcho(command, params)
        #检查是否需要动态的执行命令
        while self.hasInput:
            s = raw_input("enter your command: ")
            if s == "quit":
                break
            index = s.rfind("|");
            command = s[0:index]
            param = eval(s[(index + 1):len(s)])
            self.sendAndEcho(command, param)

        self.close()


    def sendAndEcho(self, command, params = {}):
        print("send: ",command,", params:",params)
        return self.client.sendAndEcho(command, params)

    def sendJsonAndEcho(self, command, jsonData = ""):
        print("send: ",command,", jsonData:",jsonData)
        return self.client.sendJsonAndEcho(command, jsonData)

    def close(self):
        try:
            self.client.close()
        except:
            print("close client error!")
            pass


if __name__ == "__main__":
    t = Task()
    task = Task("1", "1", ifCreateUser=True)

    task.start()
