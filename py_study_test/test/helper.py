# encoding:utf-8

import configparser
import json
import threading
import datetime


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


class InterfaceInfo:
    def __init__(self, name: str):
        # 协议名称
        self.name = name
        # 请求成功次数
        self.success = 0
        # 请求失败次数
        self.fail = 0
        # 最小请求时间
        self.minTime = 0
        # 最大请求时间
        self.maxTime = 0
        # 平均请求时间
        self.avgTime = 0

        self.lock = threading.Lock()

    """
    更新记录
    """
    def update_record(self, is_success: bool, access_time: int) -> None:
        try:
            # self.lock.acquire()
            if is_success:
                self.minTime = min(self.minTime, access_time)
                self.maxTime = max(self.maxTime, access_time)
                self.avgTime = ((self.avgTime * self.success) + access_time) / (self.success + 1)
                self.success += 1
            else:
                self.fail += 1
        except RuntimeError as e:
            print("update_record error...")
        finally:
            pass
            # self.lock.release()

class RecordInfo:
    def __init__(self, startTime: int, endTime: int):
        # 压测开始时间
        self.startTime = startTime
        # 压测结束时间
        self.endTime = endTime
        # 压测模块: 数量
        self.force_modules_record_dict = {}
        # 总请求次数
        self.total = 0
        # 请求失败总次数
        self.fail = 0
        # 失败协议: 总次数
        self.fail_dict = {}
        # 总平均请求时间
        self.avgTime = 0
        # 平均请求时间最长协议
        self.maxAvgTimeName = ""
        # 平均请求最长时间
        self.maxAvgTime = 0

    def update_record(self, interface_info_dict: dict):
        # 总成功次数
        success = 0
        # 总请求消耗时间
        total_time = 0

        for key in interface_info_dict:
            info = interface_info_dict[key]
            obj = self.__json_obj(info)
            if obj is None:
                continue

            success += obj.success
            total_time += obj.success * obj.avgTime

            self.fail += obj.fail

            fail = 0
            if self.fail in self.fail_dict:
                fail = self.fail_dict[self.fail]
            self.fail_dict[self.fail] = fail + obj.fail

            if obj.avgTime > self.maxAvgTime:
                self.maxAvgTimeName = obj.name
                self.maxAvgTime = obj.avgTime



        self.total = success + self.fail

        if success != 0:
            self.avgTime = total_time / success

        # 写日志
        self.__write_log()


    def __json_obj(self, json):
        obj = InterfaceInfo(json["name"])
        obj.success = json["success"]
        obj.fail = json["fail"]
        obj.minTime = json["minTime"]
        obj.maxTime = json["maxTime"]
        obj.avgTime = json["avgTime"]
        return obj

    # 写日志
    def __write_log(self):
        with open(r"./record.log", "a+", encoding='utf-8') as file:
            file.writelines("本次压测结果汇总如下: \n")
            t = self.endTime - self.startTime
            start = datetime.datetime.fromtimestamp(self.startTime)
            end = datetime.datetime.fromtimestamp(self.endTime)
            file.writelines(f"压测开始时间：{start}, 压测结束时间：{end}, 总耗时：{t} 秒\n")
            file.writelines(f"压测模块有如下： \n")
            str = ""
            for key in self.force_modules_record_dict:
                value = self.force_modules_record_dict[key]
                str += f"{key}, 玩家数：{value}; "
            file.writelines(f"{str}\n")
            file.writelines(f"总请求次数: {self.total}, 请求失败总次数: {self.fail} , 失败协议汇总如下: \n")
            str = ""
            for key in self.fail_dict:
                value = self.fail_dict[key]
                if value == 0:
                    str += f"     失败次数：{value}; "
                else:
                    str += f"     {key}, 失败次数：{value}; "
            file.writelines(f"{str}\n")
            avgTime = int(self.avgTime)
            file.writelines(f"总平均请求时间: {avgTime} 毫秒 \n")
            maxAvgTime = int(self.maxAvgTime)
            file.writelines(f"平均请求时间最大协议: {self.maxAvgTimeName} , 平均请求最长时间为: {maxAvgTime} 毫秒 \n")
            file.writelines("汇总结束 ------------------------------------------------------> \n\n\n")