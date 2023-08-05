# -*-coding:utf-8-*-
import dbutil
import os
import sys
from jinja2 import *
import zlib
from array import array
import datetime

'''
tabletopojo是将数据表转换成domain类的工具
'''

# 查询列信息
COLUMN_INFO = '''
SELECT  COLUMN_NAME AS "lm", 
        COLUMN_COMMENT AS "sm", 
        DATA_TYPE AS "dt", 
        IS_NULLABLE AS "isnull", 
        COLUMN_KEY AS "KEY", 
        COLUMN_DEFAULT AS "default", 
        EXTRA AS "extra"  
FROM    information_schema.columns 
WHERE   table_schema = '%s' AND TABLE_NAME = '%s'
'''


TYPE_NAME = 1
FIELD_NAME = 2
METHOD_NAME = 3

TYPE_MAP = {'varchar': 'String',
            'int': 'int',
            'text': 'String',
            'datetime': 'Date',
            'date': 'Date',
            'timestamp': 'Date',
            'bigint': 'long',
            'smallint': 'int',
            'tinyint': 'int',
            'mediumint': 'int',
            'bit': 'int',
            'float': 'float',
            'double': 'double',
            'mediumtext': 'String',
            'blob': 'byte[]'
            }

TYPE_OBJ_MAP = {'varchar': 'String',
                'int': 'Integer',
                'text': 'String',
                'datetime': 'Date',
                'timestamp': 'Date',
                'bigint': 'Long',
                'smallint': 'Integer',
                'tinyint': 'Integer',
                'mediumint': 'Integer',
                'bit': 'Integer',
                'float': 'Float',
                'double': 'Double',
                'mediumtext': 'String',
                'blob': 'byte[]',
                'long': 'Long'
                }


def crc16(content):
    b = 0xA001
    a = 0xFFFF

    t = array("B", str(content))
    for byte in t:
        a = a ^ byte
        for i in range(8):
            last = a & 0x01
            a = a >> 1
            if last == 1:
                a = a ^ b
    return a


def tableToClass(fieldName):
    strs = fieldName.split('_')
    result = ''
    for str in strs:
        result = result + str.capitalize()
    return result


def getResultMapName(className):
    return className + "ResultMap"


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
    return result;


def getter(columnName):
    strs = columnName.split('_')
    result = ''
    for str in strs:
        result = result + str.capitalize()
    return "get" + result


def setter(columnName):
    strs = columnName.split('_')
    result = ''
    for str in strs:
        result = result + str.capitalize()
    return "set" + result


class Loader(BaseLoader):
    is_usable = True
    env = Environment(loader=FileSystemLoader("."))
    env.template_class = Template
    env.globals['tableToClass'] = tableToClass
    env.globals['getResultMapName'] = getResultMapName
    env.globals['columnNameToFieldName'] = columnNameToFieldName
    env.globals['len'] = len
    env.globals['getter'] = getter
    env.globals['setter'] = setter


'''
将表转换位POJO
@param db  数据库
@param host IP地址
@param user 用户名
@param password  密码
@param tables 表的转换配置
'''


def convert(
        host='10.5.201.56',
        user='root',
        password='1234',
        tables={},
        datagetter=[],
        datagetterName=[[]],
        handleList=[[]]):
    array = range(2)
    for idx in array:
        currDataGetter = datagetter[idx]
        currDatagetterName = datagetterName[idx]
        currHandleList = handleList[idx]

        for tableName in currHandleList:
            for config in tables:
                if config['tableName'] == tableName:
                    util = dbutil.DBUtil(host=host, db=config['db'], user=user, passwd=password)
                    doTable(config['db'], util, currDataGetter, currDatagetterName, config)


'''
处理具体每一个table
'''


def doTable(db, util, datagetterpath, datagetterName, config):
    tableName = config['tableName']
    path = config['path']
    print("handle table", tableName)

    tabledesc = util.query(COLUMN_INFO % (db, tableName))
    filepath = os.path.join(sys.path[0], path, "domain\\")
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    # 定义一个字符串Buff
    fields = []
    idColumn = None
    crcstr = ""
    autoId = False
    for row in tabledesc:
        columnName = ''
        comment = ''
        type = ''
        isKey = False
        autoGenerator = False
        for (key, value) in row.iteritems():
            if value == None:
                value = ''
            value = value
            if key == 'lm':
                columnName = value
            if key == 'sm':
                comment = value
            if key == 'dt':
                type = value
            if key == 'KEY':
                isKey = value == 'PRI'
            if key == "extra":
                autoGenerator = value == "auto_increment"
                autoId = autoId or autoGenerator
        # print(columnName, comment, type, isKey)
        columnName = columnName.lower()
        typeName = getType(type)
        crcstr = crcstr + columnNameToFieldName(columnName)
        comment = getComment(comment, columnNameToFieldName(columnName))
        if isKey:
            idColumn = (columnName, typeName, isKey, comment, autoGenerator)

        fields.append((columnName, typeName, isKey, comment, autoGenerator))

    # crc = crc16(crcstr)
    if config['domainable']:
        # 载入模板环境
        env = Loader().env
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 获取自定义内容
        domainpath = filepath + getName(tableName, TYPE_NAME) + ".java"
        customContent, importContent = getCustomContent(domainpath)

        # 生成domain文件
        template = env.get_template("domain.java.template")
        result = template.render(tableName=tableName,
                                 fields=fields,
                                 packageName=getPackageName(os.path.join(path, "domain\\")),
                                 autoId=autoId,
                                 time=now,
                                 tableConfig=config,
                                 customContent=customContent,
                                 importContent=importContent)

        domainfile = open(domainpath, 'wb')
        domainfile.write(result.encode('utf8'))
        domainfile.flush()
        domainfile.close()

    createDao = False
    isSdata = False
    if config['daoable']:
        if path.find("sdata") != -1:
            isSdata = True

        if not isSdata:
            daopath = os.path.join(sys.path[0], path, "data\\")
            if not os.path.exists(daopath):
                os.makedirs(daopath)

            # 生成manager文件
            template = env.get_template("manager.java.template")
            daopath = daopath + getName(tableName, TYPE_NAME) + "Manager.java"
            if not (os.path.exists(daopath)):
                # 不存在时候生成
                # 生成Dao文件
                result = template.render(tableName=tableName,
                                         idType=config.get('daoType', "Integer"),
                                         packageName=getPackageName(os.path.join(path, "data\\")),
                                         basePackage=getPackageName(path))

                daofile = open(daopath, 'wb')
                daofile.write(result.encode('utf8'))
                daofile.flush()
                daofile.close()

                createDao = True
        else:
            daopath = os.path.join(sys.path[0], path, "cache\\")
            if not os.path.exists(daopath):
                os.makedirs(daopath)

            # 生成manager文件
            template = env.get_template("sdatacache.java.template")
            daopath = daopath + getName(tableName, TYPE_NAME) + "Cache.java"
            if not (os.path.exists(daopath)):
                # 不存在时候生成
                # 生成Dao文件
                idType = getType(idColumn[1], map=TYPE_OBJ_MAP)
                result = template.render(tableName=tableName,
                                         idType=idType,
                                         idGetter=getter(idColumn[0]),
                                         packageName=getPackageName(os.path.join(path, "cache\\")),
                                         basePackage=getPackageName(path))

                daofile = open(daopath, 'wb')
                daofile.write(result.encode('utf8'))
                daofile.flush()
                daofile.close()

                createDao = True

    if createDao:
        # DataGetter
        idatagetterpath = os.path.join(datagetterpath, datagetterName[0])
        datagetterpath = os.path.join(datagetterpath, datagetterName[1])
        if os.path.exists(idatagetterpath) and os.path.exists(datagetterpath):
            # 生成IDataGetter
            headerContent, importContent, classContent, autoContent, leftContent = getDateGetterInterfaceContent(
                idatagetterpath)
            daoName = None
            daoPackage = None
            if not isSdata:
                daoName = getName(tableName, TYPE_NAME) + "Manager"
                daoPackage = getPackageName(os.path.join(path, "data\\")) + "." + daoName
            else:
                daoName = getName(tableName, TYPE_NAME) + "Cache"
                daoPackage = getPackageName(os.path.join(path, "cache\\")) + "." + daoName

            template = env.get_template("idatagetter.java.template")
            result = template.render(headerContent=headerContent.decode('utf8'),
                                     importContent=importContent.decode('utf8'),
                                     classContent=classContent.decode('utf8'),
                                     autoContent=autoContent.decode('utf8'),
                                     leftContent=leftContent.decode('utf8'),
                                     daoName=daoName,
                                     daoPackage=daoPackage)

            file = open(idatagetterpath, 'wb')
            file.write(result.encode('utf8'))
            file.flush()
            file.close()

            # 生成DataGetter
            headerContent, importContent, classContent, autoContent1, autoContent2, leftContent1, leftContent2 = getDateGetterContent(
                datagetterpath)
            template = env.get_template("datagetter.java.template")
            result = template.render(headerContent=headerContent.decode('utf8'),
                                     importContent=importContent.decode('utf8'),
                                     classContent=classContent.decode('utf8'),
                                     autoContent1=autoContent1.decode('utf8'),
                                     autoContent2=autoContent2.decode('utf8'),
                                     leftContent1=leftContent1.decode('utf8'),
                                     leftContent2=leftContent2.decode('utf8'),
                                     daoName=daoName,
                                     daoPackage=daoPackage,
                                     isSdata=isSdata)

            file = open(datagetterpath, 'wb')
            file.write(result.encode('utf8'))
            file.flush()
            file.close()


'''
获取comment注释
'''


def getComment(comment, fieldName):
    if comment == None or comment.strip() == '':
        fieldName

    return comment.strip()


'''
获取用户自定义内容
'''


def getCustomContent(path):
    if os.path.exists(path):
        file = open(path, 'r')
        content = ""
        importContent = ""
        startFlag = False
        for line in file.readlines():
            if line == None:
                continue
            if line.strip().startswith("// Not Auto-generated Code Start"):
                startFlag = True
                continue
            if line.strip().startswith("// Not Auto-generated Code End"):
                break
            if line.strip().startswith("import"):
                importContent = importContent + line

            if startFlag and line.strip() != "":
                content = content + line

        return content.strip(), importContent.strip()

    else:
        return "", ""


'''
获取datagetter接口内容
'''


def getDateGetterInterfaceContent(path):
    file = open(path, 'r')
    headerContent = ""
    importContent = ""
    autoContent = ""
    leftContent = ""
    classContent = ""

    flag = 0
    for line in file.readlines():
        if line == None:
            continue
        if line.strip().startswith("import"):
            flag = 1
            importContent = importContent + line
            continue
        if line.strip().startswith("// Auto-generated Code Start"):
            flag = 2
            continue
        if line.strip().startswith("// Auto-generated Code End"):
            flag = 3
            continue

        if flag == 0:
            headerContent = headerContent + line
        elif flag == 1:
            classContent = classContent + line
        elif flag == 2:
            autoContent = autoContent + line
        elif flag == 3:
            leftContent = leftContent + line

    # print "headerContent", headerContent
    # print "importContent", importContent
    # print "classContent", classContent
    # print "autoContent", autoContent
    # print "leftContent", leftContent
    return headerContent.strip(), importContent.strip(), classContent.strip(), autoContent.strip(), leftContent.strip()


'''
获取datagetter内容
'''


def getDateGetterContent(path):
    file = open(path, 'r')
    headerContent = ""
    importContent = ""
    autoContent1 = ""
    autoContent2 = ""
    leftContent1 = ""
    leftContent2 = ""
    classContent = ""
    autoType = 0
    flag = 0
    for line in file.readlines():
        if line == None:
            continue
        if line.strip().startswith("import"):
            flag = 1
            importContent = importContent + line
            continue
        if line.strip().startswith("// Auto-generated Code Start"):
            if autoType == 0:
                autoType = 1
            else:
                autoType = 2
            flag = 2
            continue
        if line.strip().startswith("// Auto-generated Code End"):
            flag = 3
            continue

        if flag == 0:
            headerContent = headerContent + line
        elif flag == 1:
            classContent = classContent + line
        elif flag == 2 and autoType == 1:
            autoContent1 = autoContent1 + line
        elif flag == 2 and autoType == 2:
            autoContent2 = autoContent2 + line
        elif flag == 3 and autoType == 1:
            leftContent1 = leftContent1 + line
        elif flag == 3 and autoType == 2:
            leftContent2 = leftContent2 + line

    # print "headerContent", headerContent
    # print "importContent", importContent
    # print "classContent", classContent
    # print "autoContent", autoContent
    # print "leftContent", leftContent
    return headerContent.strip(), importContent.strip(), classContent.strip(), autoContent1.strip(), autoContent2.strip(), leftContent1.strip(), leftContent2.strip()


'''
获取包名
'''


def getPackageName(path):
    path = path.replace('..', '')
    path = path.replace('\\', '.')
    if (path.startswith('.')):
        path = path[1:]

    if (path.startswith('src')):
        return path[4:][:-1]

    return path


def getType(type, map=TYPE_MAP):
    result = map[type]
    if result == None:
        return type
    return result


def getName(fieldName, type):
    strs = fieldName.split('_')
    result = ''
    index = 1
    for str in strs:
        if type == TYPE_NAME or type == METHOD_NAME:
            result = result + str.capitalize()
        elif type == FIELD_NAME:
            if index == 1:
                result = result + str[0].lower() + str[1:]
            else:
                result = result + str.capitalize()
        index = index + 1
    return result;


if __name__ == "__main__":
    convert(
        host='10.9.200.244',
        user='root',
        password='qwert',
        tables=[
            # game
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "user",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\user\\",
                "indexs": [
                    {"name": "username", "fields": ["userName"], "unique": "true"}
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_invite",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "clubid_playerid", "fields": ["clubId", "playerId"], "unique": "false"},
                    {"name": "playerid_clubid", "fields": ["playerId", "clubId"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_member",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "clubid_type", "fields": ["clubId", "type"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_order",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_apply",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "clubid_playerid", "fields": ["clubId", "playerId"], "unique": "true"},
                    {"name": "playerid_clubid", "fields": ["playerId", "clubId"], "unique": "false"}
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "mail",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\mail\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_awake_consume_unit",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\unit\\",

            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_skill",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\structure\\",
                "indexs": [
                    {"name": "playerid_type", "fields": ["playerId", "type"], "unique": "true"}
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_unit",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\unit\\",
                "indexs": [
                    {"name": "playerid_unitid", "fields": ["playerId", "unitId"], "unique": "false"}
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_unit_group",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\unit\\",
                "indexs": [
                    {"name": "playerid_groupid", "fields": ["playerId", "groupId"], "unique": "false"}
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_friend",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\friend\\",
                "indexs": [
                    {"name": "unq_playerid_friendid", "fields": ["playerId", "friendId"], "unique": "true"},
                    {"name": "playerid_status", "fields": ["playerId", "status"], "unique": "false"},
                    {"name": "friendid_status", "fields": ["friendId", "status"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_friend_info",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\friend\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_group",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\friend\\",
                "indexs": [
                    {"name": "create_playerid", "fields": ["createPlayerId"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_group_info",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\friend\\",
                "indexs": [
                    {"name": "playerid_status", "fields": ["playerId", "status"], "unique": "false"},
                    {"name": "groupid_status", "fields": ["groupId", "status"], "unique": "false"},
                    {"name": "unq_playerid_groupid", "fields": ["playerId", "groupId"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_chat",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\chat\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_science",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\science\\",
                "indexs": [
                    {"name": "playerid_type_cityno", "fields": ["playerId", "type","cityNo"], "unique": "true"},
                    {"name": "playerid_tab", "fields": ["playerId", "tab"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_union",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "unq_clubid_unionclubid", "fields": ["clubId", "unionClubId"], "unique": "true"},
                    {"name": "clubid_state", "fields": ["clubId", "state"], "unique": "false"},
                    {"name": "unionclubid_state", "fields": ["unionClubId", "state"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_attribute",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\player\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_club_info",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\player\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_resource",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\player\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_task",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\task\\",
                "indexs": [
                    {"name": "playerid_taskid", "fields": ["playerId", "taskId"], "unique": "true"},
                    {"name": "playerid_type_status", "fields": ["playerId", "type"], "unique": "false"},
                    {"name": "playerid_chapter", "fields": ["playerId", "chapter"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_branch_task",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\task\\",
                "indexs": [
                    {"name": "playerid_taskid", "fields": ["playerId", "taskId"], "unique": "true"},
                    {"name": "playerid_type_status", "fields": ["playerId", "type"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_transport",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\transport\\",

            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "world_player_structure",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\world\\",
                "indexs": [
                    {"name": "idx_playerid_type", "fields": ["playerId", "type"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "world_npc_city_structure",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\world\\",
                "indexs": [
                    {"name": "idx_clubid", "fields": ["clubId"], "unique": "false"},
                    {"name": "idx_playerid", "fields": ["playerId"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "defend_troop",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\world\\",
                "indexs": [
                    {"name": "unq_troopid", "fields": ["troopId"], "unique": "true"},
                    {"name": "playerid_state", "fields": ["playerId","state"], "unique": "false"},
                    {"name": "defend_playerid_state", "fields": ["defendPlayerId","state"], "unique": "false"},
                    {"name": "reference_point_state", "fields": ["referencePoint","state"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_shop",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "playerid_goodsid", "fields": ["playerId","goodsId"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_help",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "unq_playerid_science_type", "fields": ["playerId","playerScienceType"], "unique": "true"},
                    {"name": "clubid_state", "fields": ["clubId","state"], "unique": "false"},
                    {"name": "playerid_type_state", "fields": ["playerId","type","state"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_science",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "unq_clubid_type", "fields": ["clubId","type"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_advance",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "unq_reference_point", "fields": ["referencePoint"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_rank_military",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\rank\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_military_shop",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\player\\",
                "indexs": [
                    {"name": "playerid_goodsid", "fields": ["playerId","goodsId"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_military_shop_info",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\player\\",

            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_task",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\club\\",
                "indexs": [
                    {"name": "unq_clubid_taskid", "fields": ["clubId","taskId"], "unique": "true"},
                    {"name": "clubid_type_status", "fields": ["clubId","type","status"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_explore",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\unit\\",
            },

            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_rank_score",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\rank\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_rank_battle_point",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\rank\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_rank_score",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\rank\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "club_rank_battle_point",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\rank\\",
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_collect_fire",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\collect\\",
                "indexs": [
                    {"name": "playerid_type", "fields": ["playerId","type"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_commander",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\commander\\",
                "indexs": [
                    {"name": "unq_playerid_commanderid", "fields": ["playerId","commanderId"], "unique": "true"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_commander_skill",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\commander\\",
                "indexs": [
                    {"name": "playerid_skillid", "fields": ["playerId","skillId"], "unique": "false"},
                    {"name": "playercommanderid_source", "fields": ["playerCommanderId","source"], "unique": "false"},
                    {"name": "playerid_source_state", "fields": ["playerId","source","state"], "unique": "false"},
                ]
            },
            {
                "db": "lz_sbtj_cn_game",
                "tableName": "player_explore_shop",
                "domainable": True,
                "daoable": True,
                "lockable": True,
                "path": "..\\src\\com\\reign\\sbtj\\unit\\",
                "indexs": [
                    {"name": "unq_playerid_goodsid", "fields": ["playerId","goodsId"], "unique": "true"},
                ]
            },


            # sdata  ---------------------------------------------------------------------------------->
            {
                "db": "xed_sbtj_cn_sdata",
                "tableName": "structure",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "xed_sbtj_cn_sdata",
                "tableName": "npc_unit",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "npc_unit2",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "npc_unit_skill",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "lz_sbtj_cn_sdata",
                "tableName": "constant",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "npc_unit2_compose",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "task",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "serial",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "resource_tips",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "guild_shop",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "guild_lv",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "guild_sci",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "guild_task",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "guild_order",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "city",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "client_effect_intro",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "item",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "military_shop",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "task_branch_head",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "task_branch",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "land",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "military_rank_score",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "guild_advance_task",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "commander",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "explore_shop",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "npc_unit2_star_param",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },
            {
                "db": "cehua_sbtj_cn_sdata",
                "tableName": "npc_unit2_param",
                "domainable": True,
                "daoable": True,
                "lockable": False,
                "path": "..\\src\\com\\reign\\sbtj\\sdata\\",
            },

        ],

        datagetter=[
            '..\\src\\com\\reign\\sbtj\\common\\data\\',
            '..\\src\\com\\reign\\sbtj\\common\\data\\',
        ],

        datagetterName=[
            ["IDataGetter.java", "DataGetter.java"],
            ["IDataGetter.java", "DataGetter.java"],
        ],

        handleList=[
            [
                #            "user",
                #            "club_member",
                #            "club_order",
                #            "club_invite",
                #            "club",
                #            "club_apply",
                #            "club_shop",
                #            "club_help",
                #            "club_science",
                #            "club_advance",
                #            "club_rank_military",
                #            "mail",
                #            "player_awake_consume_unit",
                #            "player_skill",
                #            "player_unit",
                #            "player_unit_group",
                #            "player_friend",
                #            "player_friend_info",
                #            "player_group",
                #            "player_group_info",
                #            "player_chat",
                #            "player_science",
                #            "club_union",
                #            "player_attribute",
                #            "player_club_info",
                #            "player_resource",
                #            "player_task",
                #            "player_branch_task",
                #            "player_transport",
                #            "world_player_structure",
                #            "world_npc_city_structure",
                #            "defend_troop",
                #            "player_military_shop",
                #            "player_military_shop_info",
                #            "club_task",
                #            "player_explore",
                #            "player_rank_score",
                #            "player_rank_battle_point",
                #            "club_rank_score",
                #            "club_rank_battle_point",
                #            "player_collect_fire",
                #            "player_commander",
                #            "player_commander_skill",
                #            "player_explore_shop",

            ],
            [
                #            "structure",
                #            "npc_unit",
                #            "npc_unit2",
                #            "npc_unit_skill",
                #            "constant",
                #            "npc_unit2_compose",
                #            "task",
                #            "serial",
                #            "resource_tips",
                #            "guild_shop",
                #            "guild_lv",
                #            "guild_sci",
                #            "guild_task",
                #            "guild_order",
                #            "city",
                #            "client_effect_intro",
                #            "item",
                #            "military_shop",
                #            "task_branch_head",
                #            "task_branch",
                #            "land",
                #            "military_rank_score",
                #            "guild_advance_task",
                #            "commander",
                #            "explore_shop",
                #            "npc_unit2_star_param",
                #            "npc_unit2_param",
            ]
        ])
