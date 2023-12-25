# encoding: utf-8

import sys

# Your Python script logic here

# Set the exit code
# 设置默认编码为 UTF-8
import threading

sys.stdout.reconfigure(encoding='utf-8')
# dict = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
# print(dict)
# print("AllRoomAllFishForceModule:全房间打鱼;AllRoomOnlyBossForceModule:全房间只打BOSS;ManyRobotForceModule:渔场加入多个陪玩机器人（1桌子1玩家N机器人）;OneRobotForceModule:渔场加入1个陪玩机器人（1桌子1玩家1机器人）;WarOrderForceModule:战令压测模块;")
# sys.exit(99999)

# python -c "from command import my_function; my_function()"

# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); from command import get_all_force_module_info; get_all_force_module_info()"
# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); import command; command.get_all_force_module_info()"


"""
获取所有压测模块信息
"""
# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); from command import get_all_force_module_info; get_all_force_module_info()"
def get_all_force_module_info():
    # # 设置默认编码为 UTF-8
    # sys.stdout.reconfigure(encoding='utf-8')
    # info = force.get_all_force_module_info()
    # print(info)
    pass

# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); from command import set_config; set_config('serverConfig#choose_server_config=force_stress_1;forceConfig#force_modules=OneRobotForceModule:10')"
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

# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); from command import start_force_api_test; start_force_api_test()"
def start_force_api_test():
    # 设置默认编码为 UTF-8
    # sys.stdout.reconfigure(encoding='utf-8')
    # task = force.ForceTask()
    # task.start()
    # print("start force test ....")
    pass



if __name__ == '__main__':
    # 获取正在运行的线程（此时应包含主线程和 my_thread）
    running_threads = threading.enumerate()

    # 打印线程信息
    for thread in running_threads:
        print(f"Thread Name: {thread.name}")