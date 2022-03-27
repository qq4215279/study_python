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
from jinja2 import *

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
        if jsonObj.has_key('state'):
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

#任务
class Task(threading.Thread):
    def __init__(self, name = "", password = "", title = u"标题", hasInput = False):
        threading.Thread.__init__(self)
        self.name = name
        self.password = password
        self.client = None
        self.msg = []
        self.title = title

    #执行并处理缓存
    def excuseWithRtn(self, command, param, methodName=u"方法名"):
        r,c,p = self.excuseCommand(command, param)
        method = {}
        method["name"] = methodName
        method["command"] = command
        method["index"] = 1
        #简化返回
        if r.has_key('state'):
            state = r['state']
            if state == 1:
                r = self.simpleRtn(r)
                method["rtn"] = json.dumps(r, indent=4, ensure_ascii=False)
            else:
                method["rtn"] = u"待完善"
        else:
            r = self.simpleRtn(r)
            method["rtn"] = json.dumps(r, indent=4, ensure_ascii=False)
        #分割参数
        method["params"] = []
        for k,v in param.iteritems():
            method["params"].append(k)
        self.msg.append(method)

    #简化返回
    def simpleRtn(self, r):
        if isinstance(r, list) or isinstance(r, tuple):
            r = r[0:1]
            r[0] = self.simpleRtn(r[0])
        elif isinstance(r, dict):
            for k,v in r.iteritems():
                r[k] = self.simpleRtn(v)
        return r

    ##生成文档
    def buildMDDoc(self, templeName):
        env = Environment( loader=FileSystemLoader("."))
        env.trim_blocks = True
        template = env.get_template(templeName)
        result = template.render(title = self.title, msg = self.msg)
        domainpath = self.title + ".md"
        domainfile = open(domainpath, 'wb')
        domainfile.write(result.encode('utf8'))
        domainfile.flush()
        domainfile.close()

    # 执行指令
    def excuseCommand(self, command, params):
        return self.sendAndEcho(command, params), command, params

    def connect2Server(self):
        self.client = Client("10.9.200.117", 8856, False)
        self.client.connect()

        # 创建用户 111
        self.sendAndEcho("user@createUser", {"userName": "%s" % self.name, "password": "%s" % self.password, "yx": "aoshitang"})

        # 用户登录
        self.sendAndEcho("user@login", {"userName":"%s"%self.name,"password":"%s"%self.password,"serverId":"aoshitang","platform":"PC"})

        # 创建角色 222
        self.sendAndEcho("player@createPlayer", {"playerName": "%s" % self.name, "teamId": "1"})
        
        # 获取角色列表
        playerId = self.sendAndEcho("player@getPlayerList",{})["data"]["playerList"][0]["playerId"]

        # 获取角色属性
        # self.sendAndEcho("player@getPlayerInfo", {"playerId":"%s"%str(playerId)})


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
