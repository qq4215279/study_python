# encoding: utf-8

import helper
from inf_test import Task

import random
import threading
import time
import inspect

# 配置文件
config_dict = helper.parse_config()

"""
压测任务
"""
class ForceTask(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.force_time = config_dict["force_time"]
        self.is_record = config_dict["is_record"]
        self.player_count = config_dict["player_count"]
        self.startTime = time.time()
        self.endTime = self.startTime + int(config_dict["force_time"])
        # 记录信息
        self.recordInfo = helper.RecordInfo(self.startTime, self.endTime)
        self.interface_info_dict = {}
        self.stop_flag = False


        self.forceModules = self.__init_force_modules()

        self.lock = threading.Lock()

    # 初始化所有压测模块
    def __init_force_modules(self):
        forceModules = []

        # 指定数量
        for moduleName, num in config_dict["force_modules"].items():
            self.__record_dict(moduleName, num)
            for i in range(num):
                forceModules.append(self.__create_obj(moduleName))

        need = max(self.player_count - len(forceModules), 0)
        test_modules = self.__get_test_modules()
        for i in range(need):
            moduleName = random.choice(test_modules)
            forceModules.append(self.__create_obj(moduleName))
            self.__record_dict(moduleName, 1)

        return forceModules

    # 记录模块分配情况
    def __record_dict(self, moduleName, num):
        total = 0

        if moduleName in self.recordInfo.force_modules_record_dict:
            total = self.recordInfo.force_modules_record_dict[moduleName]

        self.recordInfo.force_modules_record_dict[moduleName] = total + num

    # 获取所有测试模块
    def __get_test_modules(self):
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

    # 创建对象
    def __create_obj(self, class_name):
        # 根据类名获取类对象
        class_obj = globals()[class_name]

        # 使用类对象创建实例
        return class_obj(self.handle_force_task_end)

    def run(self) -> None:
        self.__start()

        while True:
            cur = time.time()
            if cur >= self.endTime and not self.stop_flag:
                self.stop()
                self.stop_flag = True
                break

            time.sleep(1)

    """
    压测开始
    """
    def __start(self):
        for module_obj in self.forceModules:
            module_obj.start()

    def stop(self):
        for module_obj in self.forceModules:
            module_obj.stopForceModule()

        time.sleep(3)
        self.recordInfo.update_record(self.interface_info_dict)

    # 结束回调
    def handle_force_task_end(self, name_alltimes_dict: dict):
        try:
            self.lock.acquire()

            for name in name_alltimes_dict.keys():
                allStartTime = name_alltimes_dict[name]
                if not name.startswith("Req"):
                    continue

                if name in self.interface_info_dict:
                    interface_info = self.interface_info_dict[name]
                else:
                    interface_info = helper.InterfaceInfo(name)
                    self.interface_info_dict[name] = interface_info.__dict__


                resName = name.replace("q", "s", 1) + ": "
                allResStartTime = name_alltimes_dict[resName]

                for i in range(len(allStartTime)):
                    start = allStartTime[i - 1]
                    end = allResStartTime[i - 1]
                    if end == -1:
                        interface_info.fail += 1
                    else:
                        interface_info.success += 1

                    interface_info.update_record(end != -1, (end - start))

        except RuntimeError as e:
            pass
        finally:
            self.lock.release()


"""
压测模块
"""
class ForceModule(threading.Thread):
    def __init__(self, force_task_callback):
        threading.Thread.__init__(self)
        # 是否终止线程
        self.stop = False
        self.first = True
        self.task = Task(self.handle_receive, self.handle_module_end)
        self.force_task_callback = force_task_callback


    def run(self):
        while(True):
            if self.stop:
                break

            self.__before_test()
            self._do_test()

            print(threading.current_thread().getName(), " 休眠1s~")
            time.sleep(1)

    def stopForceModule(self):
        self.stop = True

    """
    添加命令
    """
    def add_command(self, protocol_name: str, params: list):
        self.task.add_command(protocol_name, params)


    """
    测试前操作
    """
    def __before_test(self):
        if not self.first:
            return

        self.first = False

        self._do_before_test()

        # 开始任务
        self.task.start()

    """
    do 测试前操作
    """
    def _do_before_test(self):
        pass

    """
    开始压测
    """
    def _do_test(self):
        pass


    """
    处理回调
    """
    def handle_receive(self, protocal_name: str, res: dict):
        print("handle_receive....")
        print(protocal_name, res)
        pass

    """
    处理结束
    """
    def handle_module_end(self, name_alltimes_dict: dict):
        print("handle_module_end....")
        self.force_task_callback(name_alltimes_dict)
        pass

'''
战令压测模块
'''
class WarOrderForceModule(ForceModule):
    def _do_before_test(self):
        pass

    def _do_test(self):
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


    # def handle_receive(self, protocal_name: str, res: dict):
    #     pass



import atexit
def callback_function():
    print("Callback function called.")


if __name__ == '__main__':
    task = ForceTask()

    task.start()

    # 注册回调函数
    atexit.register(callback_function)