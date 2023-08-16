# encoding:utf-8

import configparser
import json

"""
帮助类
"""

"""
解析配置文件
"""


def parse_config():
    # 配置文件信息
    config_dict = {}

    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read('./config/api.ini')

    # 遍历所有节
    for section in config.sections():
        # print(f"Section: {section}")

        # 遍历当前节中的所有配置项
        for option in config.options(section):
            value = config.get(section, option)
            # print(f"{option} = {value}")

            if option.find("port") != -1 or option.find("is_create_player") != -1 or option.find("is_record") != -1 or option.find("player_count") != -1:
                config_dict[option] = int(value)
            elif option.find("force_modules") != -1:
                force_modules_dict = {}
                arr = value.split(";")
                for i in range(len(arr)):
                    arr2 = arr[i].split(":")
                    force_modules_dict[arr2[0]] = int(arr2[1])
                config_dict[option] = force_modules_dict
            else:
                config_dict[option] = value

    # print(config_dict)
    return config_dict


"""
读取协议
"""


def read_protocal(protocal_ip):
    # path = r"./"
    path = fr"\\{protocal_ip}\\sgp_dev\\protocalGenSG\\liuzhen\\"
    with open(path + "my_protocal_name_to_id.json", "r", encoding='utf-8') as my_protocal_name_to_id:
        global name_protocol_id_dict
        name_protocol_id_dict = json.load(my_protocal_name_to_id)
        global protocol_id_name_dict
        protocol_id_name_dict = dict(zip(name_protocol_id_dict.values(), name_protocol_id_dict.keys()))

    with open(path + "my_protocal_schemas.json", "r", encoding='utf-8') as my_protocol_id_name_dict:
        global protocol_schemas_dict
        protocol_schemas_dict = json.load(my_protocol_id_name_dict)

    return name_protocol_id_dict, protocol_id_name_dict, protocol_schemas_dict