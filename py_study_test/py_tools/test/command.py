# encoding: utf-8
import configparser
import os
import sys
import force_api_test as force

"""
获取所有压测模块信息
"""
def get_all_force_module_info():
    # 设置默认编码为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    info = force.get_all_force_module_info()
    print(info)

"""
修改压测配置文件
"""
def set_config(strs: str):
    if len(strs) <= 0 or strs == "":
        sys.exit(1)
        return

    print(strs)

    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取配置文件
    # config.read('./config/players.ini', encoding='utf-8')
    file_path = __file__
    # 获取当前目录所在绝对了路径
    dir_path = os.path.dirname(file_path)
    path = f"{dir_path}/config/api.ini"
    config.read(path)
    # config.read(path, encoding='utf-8')

    split = strs.split(";")
    for s in split:
        if s == '':
            continue
        s_split = s.split("#")
        env = s_split[0]
        split__split = s_split[1].split("=")
        key = split__split[0]
        value = split__split[1]

        if not config.has_section(env):
            config.add_section(env)
        config.set(env, key, value)

    # 将修改后的配置写回文件
    with open(path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

    sys.exit(0)

"""
开始压测
"""
def start_force_api_test():
    # 设置默认编码为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    task = force.ForceTask()
    task.start()
    print("start force test ....")
