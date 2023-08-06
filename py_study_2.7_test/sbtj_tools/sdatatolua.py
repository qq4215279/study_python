#-*-encoding:utf8-*-
#!/bin/python

import os
import hashlib
import yaml
import zipfile
import time
import sys, getopt
#import oss_util
from jinja2 import *
import datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import dbutil
import shutil

def tableToClass(fieldName):
    strs = fieldName.split('_')
    result = ''
    for str in strs:
        result = result + str.capitalize()
    return result

def columnNameToFieldName(columnName):
    strs = columnName.split('_')
    result = ''
    index = 1
    for str in strs:
        if index == 1:
            result = result + str[0].lower() + str[1:]
        else:
            result = result + str.capitalize()
        index = index + 1
    return result

class Loader( BaseLoader ):
    def __init__(self, parent):
        self.env = Environment( loader=FileSystemLoader(parent))
        self.env.template_class = Template
        self.env.globals['tableToClass'] = tableToClass
        self.env.globals['columnNameToFieldName'] = columnNameToFieldName

'''
sdata数据转换为lua
'''
class sdatatolua:
    '''
    构造函数
    '''
    def __init__(self, config):
        self.game = config['game']
        self.sdataZipPath = config['sdata_zip_path']
        self.sdataVersion = config['sdata_version']
        self.confFilePath = config['config_file_path']
        self.env = config['env']
        self.mode = config['mode']

        self.log("env:%s", self.env)
        self.log("game:%s", self.game)
        self.log("sdataZipPath:%s", self.sdataZipPath)
        self.log("sdataVersion:%s", self.sdataVersion)

        self.loadConfig()

        if self.mode == 'db':
            self.dbutil = dbutil.DBUtil(host=self.dbConf['host'], db=self.dbConf['db'], user=self.dbConf['user'], passwd=self.dbConf['password'])

        # oss客户端
        # self.oss = oss_util.oss_util(access_key_id=self.ossConf['access_key_id'],
        #                              access_key_secret=self.ossConf['access_key_secret'],
        #                              bucket_name=self.ossConf['bucket_name'],
        #                              endpoint=self.ossConf['endpoint'])
    '''
    载入配置
    '''
    def loadConfig(self):
        filepath = os.path.join(self.confFilePath, "sdata.yml")
        f = open(filepath, 'rb')
        # self.conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.conf = yaml.load(f.read())
        f.close()

        sdataBaseDir=self.conf['output_dir']
        try:
            sdataBaseDir = sdataBaseDir%self.env
        except:
            pass

        self.sdataDir = os.path.join(sdataBaseDir, self.game)
        self.ossConf = self.conf['oss']
        self.tablesConf = self.conf['tables']
        self.dbConf = self.conf['db']

    '''
    将Sdata转换为Lua
    '''
    def doSdataToLua(self):
        # 1. 检查工作空间
        self.doEnvCheck()

        # 2. 解压资源
        self.unzipSdataZip()

        # 3. 生成动更
        self.genSdataToLua()

        # 4. 清理
        self.doClean()


    '''
    环境检查
    '''
    def doEnvCheck(self):
        if not os.path.exists(self.sdataDir):
            self.log("第一次生成SdataToLua，创建目录:%s", self.sdataDir)
            os.makedirs(self.sdataDir)
        self.log("sdataDir:%s", self.sdataDir)

        # 目标路径
        self.newVersionDir = os.path.join(self.sdataDir, self.sdataVersion)
        if not os.path.exists(self.newVersionDir):
            os.makedirs(self.newVersionDir)
        self.log("sdataVersionDir:%s", self.newVersionDir)


    '''
    解压资源zip
    '''
    def unzipSdataZip(self):
        if self.mode == 'db':
            return

        if not os.path.exists(self.sdataZipPath):
            self.log("资源文件不存在, path:%s", self.sdataZipPath)
            sys.exit(2)
            return

        # 解压文件
        dynamicZipFile = zipfile.ZipFile(self.sdataZipPath, 'r')
        count = 0
        start = time.time()
        totalCount = dynamicZipFile.namelist().__len__()
        for file in dynamicZipFile.namelist():
            end = time.time()
            if end - start > 1:
                start = time.time()
                self.log("资源包解压中:%s/%s", count, totalCount)
            count += 1
            if file.endswith(".xml"):
                self.sdataXmlFile = os.path.join(self.newVersionDir, file)

            dynamicZipFile.extract(file, self.newVersionDir)
        self.log("资源包解压中:%s/%s", count, totalCount)

        dynamicZipFile.close()

        # 检查版本号
        version = self.loadVersionTxt(os.path.join(self.newVersionDir, 'version.txt'))

        if (version != self.sdataVersion):
            self.log("错误的打包静态库版本号:%s, 输入版本号：%s", version, self.sdataVersion)
            sys.exit(2)

        self.log("sdataXmlFile:%s", self.sdataXmlFile)


    '''
    生产sdataLua文件
    '''
    def genSdataToLua(self):
        if self.mode == 'db':
            self.genSdataToLuaByDB()
        else:
            self.genSdataToLuaByXML()

    '''
    生产sdataLua文件（db）
    '''
    def genSdataToLuaByDB(self):
        # 读取xml文件
        self.log("genSdataToLua")

        tablesMap = {}
        filePath = os.path.join(self.newVersionDir, 'SdataData.lua')
        f = open(filePath, 'wb')
        results = self.dbutil.query("show tables")
        for tableName in results:
            name = tableName['Tables_in_%s'%self.dbConf['db']]
            # 查看配置文件是否需要处理
            if not self.tablesConf.has_key(name):
                continue

            tableResults = self.dbutil.query("select * from %s"%name)
            datas = []
            rowKeys = self.tablesConf[name]['rowKey']
            for row in tableResults:
                dataMap = {}
                for key, value in row.iteritems():
                    dataMap[str(key)] = self.getValue(value)

                dataMap['rowData'] = ''
                for rowKey in rowKeys.split(","):
                    if dataMap['rowData'] != '':
                        dataMap['rowData'] = dataMap['rowData'] + "-" + dataMap[rowKey]
                    else:
                        dataMap['rowData'] = dataMap[rowKey]
                datas.append(dataMap)

            tableMap = {}
            tableMap['datas'] = datas
            tableMap['fields'] = self.tablesConf[name]['fields']
            tablesMap[name] = tableMap

        # 载入模板环境
        env = Loader(self.confFilePath).env
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 生成domain文件
        self.log("configFilePath:%s", self.confFilePath)
        template = env.get_template("sdatatolua.template", parent=self.confFilePath)
        result = template.render(tables=tablesMap, time=now, sdataVersion=self.sdataVersion)

        contentMD5 = self.md5(result.encode("utf-8"))

        f.write(result.encode('utf8'))
        f.write('sdata.time = "%s"\n'%now)
        f.write('sdata.version = "%s"\n'%self.sdataVersion)
        f.write('sdata.md5 = "%s"'%contentMD5)
        f.flush()


        fileMD5 = self.md5file(filePath)
        self.log("contentMD5:%s", contentMD5)
        self.log("fileMD5:%s", fileMD5)
        self.log("filePath:%s", os.path.abspath(filePath))

        # 生产zipFile
        fileList = []
        fileList.append('SdataData.lua')
        self.createZipFile(os.path.join(self.sdataDir, contentMD5+".zip"), fileList)

    '''
    生产sdataLua文件（XML）
    '''
    def genSdataToLuaByXML(self):
        # 读取xml文件
        self.log("genSdataToLua")
        domTree = ET.ElementTree(file=self.sdataXmlFile)
        root = domTree.getroot()

        filePath = os.path.join(self.newVersionDir, 'SdataData.lua')
        f = open(filePath, 'wb')
        tablesMap = {}
        for child in domTree.iter(tag='table'):
            table = child
            name = table.attrib["name"]

            # 查看配置文件是否需要处理
            if not self.tablesConf.has_key(name):
                continue

            datas = []
            for row in table:
                dataMap = {}
                for field in row:
                    key = field.attrib["name"]
                    value = field.text
                    dataMap[key] = value
                datas.append(dataMap)

            tableMap = {}
            tableMap['datas'] = datas
            tableMap['rowKey'] = self.tablesConf[name]['rowKey']
            tableMap['fields'] = self.tablesConf[name]['fields']
            tablesMap[name] = tableMap

        # 载入模板环境
        env = Loader().env
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 生成domain文件
        template = env.get_template("sdatatolua.template", self.confFilePath)
        result = template.render(tables=tablesMap, time=now, sdataVersion=self.sdataVersion)

        contentMD5 = self.md5(result.encode("utf-8"))

        f.write(result.encode('utf8'))
        f.write('sdata.time = "%s"\n'%now)
        f.write('sdata.version = "%s"\n'%self.sdataVersion)
        f.write('sdata.md5 = "%s"'%contentMD5)
        f.flush()


        fileMD5 = self.md5file(filePath)
        self.log("contentMD5:%s", contentMD5)
        self.log("fileMD5:%s", fileMD5)

    '''
    执行清理操作
    '''
    def doClean(self):
        try:
            shutil.rmtree(self.newVersionDir)
        except:
            pass

    '''
    载入version.txt
    '''
    def loadVersionTxt(self, filepath):
        # 打开version.lua
        version = None
        resFile = open(filepath, 'rb')
        for line in resFile.readlines():
            if line == None or line.strip() == "":
                continue
            line = line.strip()
            version = line.strip()
            break

        resFile.close()

        return version

    '''
    创建zipfile
    '''
    def createZipFile(self, zipFilePath, fileList):
        self.log("生成包:%s", zipFilePath)
        zFile = zipfile.ZipFile(zipFilePath, 'w', compression=zipfile.ZIP_DEFLATED)

        for filename in fileList:
            filepath = os.path.join(self.newVersionDir, filename)
            zFile.write(filepath, filename)
        #            self.log("pack zip file:%s, file:%s", zipFilePath, filename)

        zFile.close()

    '''
    拷贝文件
    '''
    def copyFile(self, filepath, filename):
        topath = os.path.join(self.out_dir, filename)
        self.execCmd("cp %s %s", filepath, topath)

    '''
    计算字符串md5
    '''
    def md5(self, content):
        m = hashlib.md5()
        m.update(content)

        return m.hexdigest()

    '''
    计算文件md5
    '''
    def md5file(self, filepath):
        m = hashlib.md5()
        md5file = open(filepath, 'rb')
        m.update(md5file.read())
        md5file.close()

        return m.hexdigest()

    '''
    执行系统命令
    '''
    def execCmd(self, cmd, *args):
        print(args)
        if args != None and len(args) > 0:
            cmd = cmd%args

        p = os.popen(cmd)
        self.log("exec cmd: %s end. rtn:%s", cmd, p.read())

    '''
    打印日志
    '''
    def log(self, fmt, *args):
        if args == None and len(args) == 0:
            return

        print(fmt%args)

    '''
    获取值
    '''
    def doSQL(self, sql):
        return sql.replace('%s', '\'' + '%s' + '\'')
    
    '''
    获取db值
    '''
    def getValue(self, value):
        valueTypeName = type(value).__name__
        rtn = None
        if valueTypeName != 'str' and valueTypeName != 'unicode':
            rtn = str(value)
        else:
            rtn = value

        if rtn.find('"') != -1:
            rtn = rtn.replace('"', '\\"')
        return rtn

def main(argv):
    config = {
        "game": "zjzr2",
        "sdata_zip_path": "C:\\Users\\wangys\\Downloads\\sdata.zip",
        "sdata_version": "0.0.0.0",
        "env": "dev",
        "mode": "db",
        "config_file_path": "tools"
    }
    try:
        opts, args = getopt.getopt(argv, "g:p:v:r:s:e:t:h:", ["game=", "path=", "version=", "region", "scope=", "env=", "tips=", "help="])
    except getopt.GetoptError:
        print('hotupdate -g <gameId> -p <resPackPath> -v <newVersion> -r <region> -s <scope> -e <env> [-t <tips>]')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-g", "--game"):
            config['game'] = arg
        elif opt in ("-p", "--path"):
            config['res_zip_path'] = arg
        elif opt in ("-v", "--version"):
            config['game_version'] = arg
        elif opt in ("-r", "--region"):
            config['region'] = arg
        elif opt in ("-s", "--scope"):
            config['scope'] = arg
        elif opt in ("-e", "--env"):
            config['env'] = arg
        elif opt in ("-t", "--tips"):
            config['update_tips'] = arg
        elif opt in ("-h", "--help"):
            print('hotupdate -g <gameId> -p <resPackPath> -v <newVersion> -r <region> -s <scope> -e <env> [-t <tips>]')
    # /home/hario/hotupdate.sh --game ${option.game} --region ${option.region} --scope ${option.scope} --version ${option.version} --env ${option.env} --isBeta ${option.isBeta} --hides ${option.hides}
    # -g gmmx -p F:/hotupdate/gmmx_cn_9.9.9.9_android_20190527180239_191_static_dynamic.zip -v 9.9.9.9 -r cn_luajit32 -u android,ast -t tips

    p = sdatatolua(config)
    p.doSdataToLua()


if __name__ == '__main__':
    main(sys.argv[1:])
