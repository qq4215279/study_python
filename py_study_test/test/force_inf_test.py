# encoding: utf-8

import api_test_helper as helper
# from .inf_test import Task
from inf_test import Task

import random
import threading
import time
import inspect
import queue

# 配置文件
config_dict = helper.parse_config()


class ForceTask:
    def __init__(self):
        self.force_time = config_dict["force_time"]
        self.is_record = config_dict["is_record"]
        self.player_count = config_dict["player_count"]
        self.force_modules = config_dict["force_modules"]

        self.forceModules = self.__init_force_modules()

    def __init_force_modules(self):
        forceModules = []

        for moduleName, num in self.force_modules.items():
            for i in range(num):
                forceModules.append(create_obj(moduleName))


        need = max(self.player_count - len(forceModules), 0)
        test_modules = get_test_modules()
        for i in range(need):
            moduleName = random.choice(test_modules)
            forceModules.append(create_obj(moduleName))

        return forceModules

    """
    压测开始
    """
    def start(self):
        for module_obj in self.forceModules:
            module_obj.start()

def get_test_modules():
    # 获取当前模块对象
    current_module = inspect.currentframe().f_globals['__name__']
    module = __import__(current_module)

    # 获取当前模块中的所有成员
    all_members = inspect.getmembers(module)
    # 筛选出类对象
    classes = [member[1] for member in all_members if inspect.isclass(member[1])]

    test_modules = []
    # 打印所有类的名称
    for cls in classes:
        class_name = cls.__name__
        if not class_name.endswith("Module"):
            continue
        if class_name == "ForceModule":
            continue
        test_modules.append(class_name)

    return test_modules

def create_obj(class_name):
    # 根据类名获取类对象
    class_obj = globals()[class_name]

    # 使用类对象创建实例
    return class_obj()


"""
压测模块
"""

class ForceModule(threading.Thread):
    def __init__(self, ):
        threading.Thread.__init__(self)
        self.first = True
        self.queue = queue.Queue()
        self.task = Task(config_dict["ip"], config_dict["port"], config_dict["env"], config_dict["is_create_player"], self.handle_receive)

    def run(self):
        while(True):
            self.before_test()
            self.do_test()

            print(threading.current_thread().getName(), " 休眠1s~")
            time.sleep(1)


    def before_test(self):
        if not self.first:
            return

        self.first = False

        self._do_before_test()

        # 开始任务
        self.task.start()



    def _do_before_test(self):
        pass

    """
    压测
    """

    def do_test(self):
        pass

    """
    添加命令
    """
    def add_command(self, protocol_name: str, params: list):
        self.task.add_command(protocol_name, params)


    def handle_receive(self, protocal_name: str, res: dict):
        print("handle_receive....")
        print(protocal_name, res)
        pass

'''
战令压测模块
'''


class WarOrderForceModule(ForceModule):

    def _do_before_test(self):
        pass

    def do_test(self):
        # 1. 获取战令信息
        self.add_command("ReqGetPlayerWarOrderInfo", [])
        # 2. 请求领取战令通行证奖励
        self.add_command("ReqGetWarOrderPassCardReward", [])

        # 3. 请求获取夏日寻访信息
        self.add_command("ReqGetSummerTourInfo", [])
        # 4. 请求寻访  寻访类型: 1: 阳光海滩; 2: 泳池派对    次数
        self.add_command("ReqDrawSummerTour", [random.randint(1, 2), random.choice((1, 10))])
        # 5. 请求领取寻访额外奖励  寻访类型: 1: 阳光海滩; 2: 泳池派对   序列
        self.add_command("ReqGetSummerTourExtraReward", [random.randint(1, 2), random.randint(1, 11)])

        # 6. 请求获取夏日探宝信息
        self.add_command("ReqGetSummerTreasureInfo", [])
        # 7. 请求夏日探宝  探宝类型: 1: 免费; 2: 普通; 3: 高级   探宝次数
        self.add_command("ReqDrawSummerTreasure", [random.randint(1, 3), random.randint(1, 100)])

        # 8. 请求领取夏日探宝累计任务奖励  需要累计探宝次数
        self.add_command("ReqGetTreasureCumulateTaskReward", [4])

        # 9. 请求获取战令任务信息
        self.add_command("ReqGetWarOrderTaskInfo", [])
        # 10. 请求领取战令任务奖励  任务id: >0: 具体任务; -1: 每日任务可领奖列表; -2: 每周任务可领奖列表; -3: 每期任务可领奖列表
        self.add_command("ReqGetWarOrderTaskReward", [random.choice((-1, -2, -3))])


import atexit
def callback_function():
    print("Callback function called.")
if __name__ == '__main__':
    task = ForceTask()

    task.start()

    # 注册回调函数
    atexit.register(callback_function)