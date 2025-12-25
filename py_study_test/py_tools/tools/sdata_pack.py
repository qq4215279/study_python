#-*-coding:utf-8-*-
import dbutil
import os
import zipfile

#查询列信息
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



#类型Map
TYPE_MAP = {'varchar':'String',
            'int':'int',
            'text':'String',
            'datetime':'Date',
            'timestamp':'Date',
            'bigint':'long',
            'smallint':'int',
            'tinyint':'int',
            'mediumint':'int',
            'bit':'int',
            'float':'float',
            'double':'double',
            'mediumtext':'String',
            'blob':'byte[]'
}

#模板
db_table = '<!-- <table name="%s"> -->%s'
db_field = '<field name="%s">%s</field>'



'''
将表转换位POJO
@param db  数据库
@param host IP地址
@param user 用户名
@param password  密码
@param tables 表的转换配置
'''
def pack(db='cehua_zjzr2_cn_sdata',
    host='10.9.200.244',
    user='root', 
    password='qwert',
    version='1.0.0.0',
    path=''):
    
    # 连接数据库
    util = dbutil.DBUtil(host=host, db=db, user=user, passwd=password)
    
    print("pack %s start"%(db))
    result = util.query('show tables')
    xml_result = []
    xml_result.append('<?xml version="1.0" encoding="utf-8"?>\r\n')
    xml_result.append('<mysql>\r\n')
    xml_result.append('<database name="%s">\r\n'%(db))
    
    for v in result:
        print ("pase table " + v.values()[0])
        doTable(db, v.values()[0], xml_result, util)
    xml_result.append('</database>\r\n')
    xml_result.append('</mysql>')


    # 文件名定义
    fileName = ""
    if db.endswith("sdata"):
        fileName = db + ".xml"
    else:
        fileName = db + "_sdata.xml"

    if not os.path.exists(path):
        os.makedirs(path)
    f = open(os.path.join(path, fileName), 'wb')
    f.write((''.join(xml_result)).encode("utf-8"))
    f.flush()
    f.close()
    
    v = open(os.path.join(path, 'version.txt'), 'wb')
    v.write(version)
    v.flush()
    v.close()

    # 打zip包
    z = zipfile.ZipFile(os.path.join(path, 'sdata.zip'), 'w', zipfile.ZIP_DEFLATED)
    z.write(os.path.join(path, fileName))
    z.write(os.path.join(path, 'version.txt'))
    z.close()

    # 删除sql
    os.remove(os.path.join(path, fileName))
    os.remove(os.path.join(path, 'version.txt'))

    util.close()
    print("pack %s succ"%(db))


def doTable(db, table, buff, util):
    # 分析Table
    tabledesc = util.query(COLUMN_INFO%(db, table))
    column_map = {}
    for row in tabledesc:
        columnName = ''
        type = ''
        for (key, value) in row.iteritems():
            if value == None:
                value = ''
            value = value
            if key == 'lm':
                columnName = value
            if key == 'dt':
                type = value
                
        typeName = getType(type)
        column_map[columnName] = typeName

    
    # 分析数据
    result = util.query('select * from %s' % table)
    buff.append('<table name="%s">%s'%(table, '\r\n'))
    for row in result:
        buff.append('<row>')
        for (key, value) in row.iteritems():
            value = getValue(key, value, column_map)
            
            buff.append(db_field%(key, value))
        
        buff.append('</row>\r\n')
    
    buff.append('</table>\r\n')

'''
获取列的数据类型
'''
def getType(type, map=TYPE_MAP):
    result = map[type]
    if result == None:
        return type
    return result    

'''
            'varchar':'String',
            'int':'int',
            'text':'String',
            'datetime':'Date',
            'timestamp':'Date',
            'bigint':'long',
            'smallint':'int',
            'tinyint':'int',
            'mediumint':'int',
            'bit':'int',
            'float':'float',
            'double':'double',
            'mediumtext':'String',
            'blob':'byte[]'

'''
def getValue(columnName, value, column_map):
    type = column_map[columnName]
    if type == "int" or type == "float" or type == "double" or type == "long":
        if value == None:
            return 0
        else:
            return value
    else:
        if value == None:
            return "null"
        elif isinstance(value, unicode):
            value = value.replace('&', '&amp;')
            if value.find('<') != -1:
                value = '<![CDATA[' + value + ']]>'

        return value
    


if __name__ == "__main__":    
    print("hello pack")
