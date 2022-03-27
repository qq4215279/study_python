# coding:utf-8

import json
import tablib

"""
将json字符串  ->  字段dict
json.loads  操作的是字符串
json.load   操作的是文件流

将字典dict  ->  json字符串
json.dumps
json.dump
"""

"""
1. json字符串 -> 字典
使用 loads() 将json字符串的res转换成方便python处理的dict   res_dict
"""
res = ''' {"key1":"123","key2":"abc"} '''
res_dict = json.loads(res)
print(res_dict)
print(type(res_dict))

print("1------->")

"""
2. 字典 -> json字符串

"""
res2 = {"关键字一号": "123", "key2": "abc"}
# res2_json = json.dumps(res2, indent=4, ensure_ascii=False)
res2_json = json.dumps(res2, indent=4, ensure_ascii=False).decode('utf8')

print(res2_json)
print(type(res2_json))
print("2------->")

"""
3. 将文件里的json内容  -> 字段dict  

"""
with open(r'jsonFile.json', "r") as jsonFile:
    # data = jsonFile.read().decode(encoding='utf-8').encode(encoding='utf-8')
    # res222 = json.loads(data)
    # print(res222)

    print("111111111111")

    res_dict = json.load(jsonFile)
    print(res_dict)
    print(type(res_dict))
    print("3------->")
"""
4. 将字典 ->  写入文件
"""
res2 = {"关键字2好": "123", "key2": "abc"}
f4 = open('testjson.txt', mode='w')  # 只写模式打开文件
# 将字典直接通过dump转换成字典后写入文件对象f，不需要转换成字典赋值给对象，然后再调用f.write()写入文件。从而更加高效的实现了文件的写入
json.dump(res2, f4, indent=4, ensure_ascii=False)
