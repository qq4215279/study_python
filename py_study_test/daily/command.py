# encoding: utf-8

import sys

# Your Python script logic here

# Set the exit code
# 设置默认编码为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')
# dict = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
# print(dict)
# print("AllRoomAllFishForceModule:全房间打鱼;AllRoomOnlyBossForceModule:全房间只打BOSS;ManyRobotForceModule:渔场加入多个陪玩机器人（1桌子1玩家N机器人）;OneRobotForceModule:渔场加入1个陪玩机器人（1桌子1玩家1机器人）;WarOrderForceModule:战令压测模块;")
# sys.exit(99999)

# python -c "from command import my_function; my_function()"

# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); from command import get_all_force_module_info; get_all_force_module_info()"
# python -c "import sys; sys.path.append('F:\\Code\\WorkSpace\\yjxxl_server\\app\\trunk\\hf-parent\\3rd-party\\py_tools\\test'); import command; command.get_all_force_module_info()"


sys.path.append("")

def my_function():
    print("Hello from my_function in mymodule")


"""
获取所有压测模块信息
"""
def get_all_force_module_info():
    # 设置默认编码为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    info = force.get_all_force_module_info()
    print(info)