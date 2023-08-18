# encoding:utf-8

import configparser
import json
import threading


"""
帮助类
"""
lock = threading.Lock()

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
        # 遍历当前节中的所有配置项
        for option in config.options(section):
            value = config.get(section, option)

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

    return config_dict



"""
读取协议
"""
def read_protocal(protocal_addr):
    # protocal_addr = r"./"
    with open(protocal_addr + "my_protocal_name_to_id.json", "r", encoding='utf-8') as my_protocal_name_to_id:
        global name_protocol_id_dict
        name_protocol_id_dict = json.load(my_protocal_name_to_id)
        global protocol_id_name_dict
        protocol_id_name_dict = dict(zip(name_protocol_id_dict.values(), name_protocol_id_dict.keys()))

    with open(protocal_addr + "my_protocal_schemas.json", "r", encoding='utf-8') as my_protocol_id_name_dict:
        global protocol_schemas_dict
        protocol_schemas_dict = json.load(my_protocol_id_name_dict)

    return name_protocol_id_dict, protocol_id_name_dict, protocol_schemas_dict

# 查找玩家账号
def find_player_account(env: str):
    need_create_player = True
    account_dict = {}
    try:
        lock.acquire()

        config_players_dict = __read_players_config(env)

        for account, value_dict in config_players_dict.items():
            # 当前账号被使用
            if value_dict["isUsed"] == 1:
                continue
            else:
                value_dict["isUsed"] = 1
                value_str = json.dumps(value_dict)
                __write_players_config(env, account, value_str)

                need_create_player = False
                account_dict = value_dict
                break

    except BaseException as e:
        print(e)
    finally:
        lock.release()
        return need_create_player, account_dict

# 记录创角账号
def add_player_account(env: str, playerId: int, account_dict={}):
    try:
        lock.acquire()
        __write_players_config(env, playerId, json.dumps(account_dict))
    except BaseException as e:
        print(e)
    finally:
        lock.release()

# 返还玩家账号
def reback_player_account(env: str, playerId: int):
    try:
        lock.acquire()
        playerId = str(playerId)
        config_players_dict = __read_players_config(env)

        value_dict = config_players_dict[playerId]
        value_dict["isUsed"] = 0

        __write_players_config(env, playerId, json.dumps(value_dict))

    except BaseException as e:
        print(e)
    finally:
        lock.release()


def __read_players_config(env: str):
    # 配置文件信息
    config_players_dict = {}

    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read('./config/players.ini', encoding='utf-8')

    # 遍历当前节中的所有配置项
    for option in config.options(env):
        value = config.get(env, option)
        # print(f" {option} = {value}")
        config_players_dict[option] = json.loads(value)

    return config_players_dict

def __write_players_config(env: str, playerId: int, value: str):
    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read('./config/players.ini', encoding='utf-8')

    if not config.has_section(env):
        config.add_section(env)
    config.set(env, str(playerId), value)

    # 将修改后的配置写回文件
    with open('./config/players.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)
