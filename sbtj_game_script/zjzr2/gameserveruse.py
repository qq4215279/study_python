#coding:utf-8
import os 
import sys
import socket
import time
import struct
import json
import copy
import random
import zlib
import threading
import hashlib
import datetime
import httplib
import urllib

usage_desc = u'''
python sc ip地址 端口号 [命令]
'''

def usage():
    print usage_desc.decode("UTF-8")


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
        
        
    def recv(self, output=False):
        # 读取包头
        if(len(self.buf) < 4):
            data = self.sock.recv(1024)
            self.buf = self.buf + data
        
        # 获取长度
        length = struct.unpack(">i",self.buf[0:4] )
        length = int(length[0])
        
        # 读取内容
        while(len(self.buf) < length + 4):
            data = self.sock.recv(1024)
            self.buf = self.buf + data
        
        # 分析包的格式
        command, id, msg = struct.unpack(">32si%ss"%(length-4-32), self.buf[4:length+4])

        # 如果服务器端压缩了，需要解压
        if self.compress:
            msg = zlib.decompress( msg )
        
        # 保留多余读取的包
        self.buf = self.buf[4 + length:]
        
        # fw = open("interface.txt" "a")
        # fw.write(msg + "")
        #a = msg.decode("utf-8").encode('gbk')
        print "recv:",msg.decode("utf-8").encode('gbk', 'replace'),"\n"
        # fw.close()

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
        for (key, value) in param.iteritems():
            if index > 1:
                data = data + "&"
            #print type(key)keytype(value)value
            data = data + key + "=" + value
            index = index + 1
        
        # print data
        
        # 组织包
    
        length = 32 + 4 + len(data)
        
        result = struct.pack(">i32si%ss"%(len(data)), length, cmd, self.requestId, data)
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
    def __init__(self, name = "", password = "", hasInput = False, ifCreateUser = True):
        threading.Thread.__init__(self)
        self.name = name
        self.password = password
        self.client = None
        self.commands = []
        self.hasInput = hasInput
        self.ifCreateUser = ifCreateUser

    def addCommand(self, command, params):
        self.commands.append((command, params))

    def run(self):
        self.client = Client("10.9.200.117", 8857, False)
        self.client.connect()

        if (self.ifCreateUser):
            # 创建用户
            self.sendAndEcho("user@createUser", {"userName":"%s"%self.name, "password":"%s"%self.password, "yx":"aoshitang"})
        #用户登录
        self.sendAndEcho("user@login", {"userName":"%s"%self.name,"password":"%s"%self.password,"serverId":"aoshitang","platform":"PC"})
        if (self.ifCreateUser):
            # 创建角色
            self.sendAndEcho("player@createPlayer", {"playerName":"%s"%self.name, "memberLine":"1"})
        # 获取角色列表
        playerId = self.sendAndEcho("player@getPlayerList",{})["data"]["playerList"][0]["playerId"]

        # 获取角色属性
        self.sendAndEcho("player@getPlayerInfo", {"playerId":"%s"%str(playerId)})

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
        print "send: ",command,", params:",params
        return self.client.sendAndEcho(command, params)

    def close(self):
        try:
            self.client.close()
        except:
            print "close client error!"
            pass
        

if __name__ == "__main__":
    t = Task()
    t.start()
