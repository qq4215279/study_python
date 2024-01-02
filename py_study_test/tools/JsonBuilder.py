#-*-coding:utf-8-*-
import os
import sys
import zlib
from jinja2 import *
from array import array


class Loader( BaseLoader ):
    is_usable = True
    env = Environment( loader=FileSystemLoader("."))
    env.template_class = Template



def readFile(path):
    f = open(path, 'r')
    msgs = {}
    stack = []
    msg = None
    for line in f.readlines():
        if line is None or line.strip() == "":
            continue
        
        if line.startswith("//"):
            continue
        
        line = line.strip()
        strs = line.split(" ")
        if strs[0] == 'message':
            if len(stack) == 0:
                msg = {}
                msg['name'] = strs[1]
                msg['columns'] = []
                msgs[msg['name']] = msg
                msg['bitFlags'] = 0
                msg['innerMsgs'] = []
                stack.append(msg)
            else:
                tempMsg = {}
                tempMsg['name'] = strs[1]
                tempMsg['columns'] = []
                tempMsg['bitFlags'] = 0
                tempMsg['innerMsgs'] = []
                msg['innerMsgs'].append(tempMsg)
                stack.append(tempMsg)
                msg = tempMsg
            if strs[2] == 'extends':
                msg['extends'] = strs[3]
            continue
        
        if strs[0] == "required":
            columInfo = parseColumn(1, strs)
            msg['columns'].append(columInfo)
            msg['bitFlags'] = msg['bitFlags'] | columInfo[3]
        elif strs[0] == "optional":
            columInfo = parseColumn(2, strs)
            msg['columns'].append(columInfo)
            msg['bitFlags'] = msg['bitFlags'] | columInfo[3]
        elif strs[0] == "repeated":
            columInfo = parseColumn(3, strs)
            msg['columns'].append(columInfo)
            msg['bitFlags'] = msg['bitFlags'] | columInfo[3]
        elif strs[0] == "}":
            stack.pop()
            if len(stack) > 0:
                msg = stack[-1]
    
    
    # 生成文件
    # 载入模板环境
    env = Loader().env
    for (key, value) in msgs.iteritems():
        print "msg:", value
        # 生成domain文件
        template = env.get_template( "message.template" )
        path = "..\\src\\com\\reign\\football2\\message\\"
        package = "com.reign.sbtj.drop.message"
        result = template.render(package = package, msg=value)
        domainpath = path + key + ".java"
        domainfile = open(domainpath, 'wb') 
        domainfile.write(result.encode('utf8'))
        domainfile.flush()
        domainfile.close()
    

def parseColumn(type, strs):
    bitFlag = 2 ** (int(strs[4]) - 1) # 位标志
    comments = "";
    if  len(strs) > 5 and strs[5] == "//":
        comments = " ".join(strs[6:]).decode("utf-8")
        #print "comments:",comments
    columInfo = (type, strs[1], strs[2], bitFlag, comments)
    return columInfo

    


if __name__ == "__main__":
    readFile(r"..\\src\\com\\reign\\football2\\message\\json\\dropExpF.json")


            
