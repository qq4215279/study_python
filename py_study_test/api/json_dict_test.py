# coding:utf-8

import json
import tablib

"""
将json字符串  ->  字段dict
json.loads(json_string)  操作的是字符串。将JSON格式的字符串解析为Python数据结构
json.load(file)   操作的是文件流。从JSON文件中读取数据并解析为Python数据结构。

将字典dict  ->  json字符串
json.dumps(dict, indent=None)：将Python数据结构转换为JSON格式的字符串。indent参数用于指定缩进级别，使生成的JSON更易读。
json.dump(dict, file)：将Python数据结构写入到JSON文件中。
    常用参数及其含义：
        obj（必需）：要转换为 JSON 的 Python 数据结构，通常是字典、列表等。
        skipkeys（可选）：如果设置为 True，则在转换过程中会跳过非字符串键的字典。默认为 False。
        ensure_ascii（可选）：如果设置为 True（默认值），则所有非 ASCII 字符将被转义为 Unicode 转义序列（比如 \\uXXXX）。
        check_circular（可选）： 如果设置为 True，则会检测并防止循环引用（对象之间相互引用）。默认为 True。
        allow_nan（可选）：如果设置为 True，则允许将 NaN、Infinity 和 -Infinity 作为 JSON 中的数字值。默认为 True。
        cls（可选）：一个定制的 JSONEncoder 子类，用于控制 JSON 格式化过程。默认为 None。
        indent（可选）：控制生成的 JSON 字符串的缩进级别，可以是一个整数表示缩进的空格数，也可以是字符串。如果设置为 None（默认值），则不进行缩进。
        separators（可选）：用于控制生成 JSON 字符串中的分隔符，是一个元组，包含 (item_separator, key_separator)。默认为 (",", ":")。
        default（可选）：如果提供，是一个函数，用于处理不可序列化的对象。通常在自定义 JSON 编码时使用。
        sort_keys（可选）：如果设置为 True，则会按照键的字母顺序对字典进行排序。默认为 False。
"""

"""
1. json字符串 -> 字典
json.loads() 将json字符串的res转换成方便python处理的dict   res_dict
"""
res = ''' {"key1":"123","key2":"abc"} '''
res_dict = json.loads(res)
print(res_dict)
print(type(res_dict))

print("1------->")

"""
2. 字典 -> json字符串
json.dumps(obj, indent=None)
"""
res2 = {"关键字一号": "123", "key2": "abc"}
res2_json = json.dumps(res2, ensure_ascii=False)
res2_json2 = json.dumps(res2, indent=4, ensure_ascii=False)

print("res2_json: ", res2_json)
print("res2_json2: ", res2_json2)
print(type(res2_json))
print("2------->")

complex_data = {
    "person": {
        "name": "Alice",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "hiking"],
        "is_student": False,
        "contact": None
    }
}

json_string = json.dumps(complex_data, indent=2)
print(json_string)

"""
3. 将文件里的json内容  -> 字段dict  
json.load(file)
"""
with open(r'../api2/file/jsonFile.json', "r", encoding='utf-8') as jsonFile:
    # data = jsonFile.read().decode(encoding='utf-8').encode(encoding='utf-8')
    # res222 = json.loads(data)
    # print(res222)

    res_dict = json.load(jsonFile)
    print(res_dict)
    print(type(res_dict))
    print("3------->")
"""
4. 将字典 ->  写入文件
json.dump(obj, api2)
"""
res2 = {"关键字2号": "123", "key2": "abc"}
f4 = open('../api2/file/testjson2.json', mode='w', encoding='utf-8')  # 只写模式打开文件
# 将字典直接通过dump转换成字典后写入文件对象f，不需要转换成字典赋值给对象，然后再调用f.write()写入文件。从而更加高效的实现了文件的写入
json.dump(res2, f4, indent=4, ensure_ascii=False)

"""
反转字典的4种方法（字典的key和value对换）
"""


def reverseDict():
    # 1. 字典推导式：
    m = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    res = {v: k for k, v in m.items()}
    print(res)

    # 2. 使用压缩器:
    mi = dict(zip(m.values(), m.keys()))
    print(mi)

    # 3. 遍历字典：
    inverted_dict = {}
    for key, value in m.items():
        inverted_dict[value] = key
    print(inverted_dict)

    # 4. 结合函数map, reversed：
    inverted_dict = dict(map(reversed, m.items()))
    print(inverted_dict)


reverseDict()
