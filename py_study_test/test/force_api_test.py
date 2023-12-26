# encoding: utf-8
import sys

import helper
from api_test import Task

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
        self.finish_stop_num = 0


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

        t_stop = threading.Thread(target=self.__run_stop())
        t_stop.start()

    def __run_stop(self):
        while True:
            if self.finish_stop_num >= len(self.forceModules):
                self.recordInfo.update_record(self.interface_info_dict)
                break
            else:
                time.sleep(1)

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
                    self.interface_info_dict[name] = interface_info


                resName = name.replace("q", "s", 1)
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
            self.finish_stop_num += 1
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
        # 休眠时间
        self.ticket = 1

    def _set_ticket(self, ticket):
        self.ticket = ticket

    def _get_ticket(self):
        return self.ticket

    def run(self):
        while(True):
            if self.stop:
                break

            # 保持心跳
            self.add_command("ReqKeepAlive", [])

            self.__before_test()
            self._do_test()


            time.sleep(self.ticket)
            print(threading.current_thread().getName(), f" 休眠{self.ticket}s~")


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
    @classmethod
    def get_force_module_name(cls):
        return "战令压测模块"

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


    def handle_receive(self, protocal_name: str, res: dict):
        pass

"""
全房间打鱼
"""
class AllRoomAllFishForceModule(ForceModule):
    def __init__(self, force_task_callback):
        super().__init__(force_task_callback)
        super()._set_ticket(0.2)

        # 是否进入房间
        self.isEnterRoom = False
        # 使用道具cd
        self.shotItemCD = 30

        self.BOSS_LIVE_TIME = 100000
        self.bulletIndex = 0
        self.currBossIndex = -1
        self.bossMap = {}
        self.roomIndex = random.randint(2, 5)
        self.tableId = 0

    @classmethod
    def get_force_module_name(cls):
        return "全房间打鱼"

    def _do_before_test(self):
        if self.gold < 10000000000:
            self.add_command("ReqGiveMeItems", [{"1001": 10000000000, "1006": 100000000, "6001": 100000000, "6113": 100000000, "4001": 9999}, helper.KEY, self.playerId])
        if self.maxCannonMultiple < 500000:
            # 升级炮倍
            self.add_command("ReqOBUnlockCannonLv", [50000, True])
            time.sleep(1)
            # 切换到50000炮倍
            self.add_command("ReqFruitChangeMultiple", [50000])
        # 进房间
        self.add_command("ReqEnterFruitRoom", [self.roomIndex, 1, 0])

    def _do_test(self):
        now = time.time()
        if self.isEnterRoom and len(self.bossMap.keys()) > 0:
            try:
                bossInfo = None
                for key, info in self.bossMap.items():
                    # if now < info["createdTime"] + self.BOSS_LIVE_TIME and now > info["createdTime"] + 5000:
                    if now < info["createdTime"] + self.BOSS_LIVE_TIME:
                        bossInfo = info
                        break

                if not bossInfo is None:
                    index = bossInfo["index"]
                    self.currBossIndex = index
                    self.add_command("ReqFruitAttack", [index, self.bulletIndex, ""])

                    self.add_command("ReqFruitHit", [self.bulletIndex, index])

                    self.__next_bulet()

                # 道具使用
                self.shotItemCD += super()._get_ticket()
                if self.shotItemCD > 30:
                     self.shotItemCD = 0
                     # 使用狂暴
                     self.add_command("ReqFruitShotItem", [1])

            except RuntimeError as e:
                print("AllRoomAllFishForceModule _do_test error")
            finally:
                pass

    def handle_receive(self, protocal_name: str, res: dict):
        if protocal_name.find("ResLoginAccount") != -1 or protocal_name.find("ResRegisterTourist") != -1:
            self.playerId = res["playerInfo"]["playerId"]
            self.gold = res["playerInfo"]["gold"]
            self.maxCannonMultiple = res["playerInfo"]["maxCannonMultiple"]
        elif protocal_name.find("ResEnterFruitRoom") != -1:
            self.tableId = res["info"]["tableId"]
            print(f" player: {self.playerId} 进入桌子 {self.tableId} 开始打鱼..")
            # 水果房间同步
            self.add_command("ReqFruitSynchGame", [])

            self.isEnterRoom = True
        elif protocal_name.find("ResFruitSynchGame") != -1:
            for info in res["bossInfoList"]:
                self.bossMap[info["index"]] = info
        elif protocal_name.find("PushFruitBossShow") != -1:
            info = res["bossInfo"]
            self.bossMap[info["index"]] = info

            now = time.time()
            for key, info in self.bossMap.items():
                if now >= info["createdTime"] + self.BOSS_LIVE_TIME:
                    del (self.bossMap[key])
        elif protocal_name.find("PushFruitAllBossDie") != -1:
            index = res["index"]
            if index in self.bossMap:
                del (self.bossMap[index])
        elif protocal_name.find("ResFruitAttack") != -1:
            # 鱼id 不存在
            if res["requestResult"] == 10121:
                if self.currBossIndex in self.bossMap:
                    del (self.bossMap[self.currBossIndex])
            # 子弹id错误
            elif res["requestResult"] == 10940:
                print(f"子弹id有误 playerId = {self.playerId} bulletIndex = {self.bulletIndex}")
                self.__next_bulet()
        elif protocal_name.find("ResFruitHit") != -1:
            # 桌子不存在
            if res["requestResult"] == 10920:
                self.bossMap.clear()
                # 重新进房间
                self.add_command("ReqEnterFruitRoom", [self.roomIndex, 1, 0])
            elif res["requestResult"] == 1:
                if res["resStatus"] != 0 and res["index"] != -1:
                    index = res["index"]
                    if index in self.bossMap:
                        del (self.bossMap[index])

    def __next_bulet(self):
        if self.bulletIndex == sys.maxsize:
            self.bulletIndex = 0
        else:
            self.bulletIndex += 1


"""
全房间只打BOSS
"""
class AllRoomOnlyBossForceModule(AllRoomAllFishForceModule):
    @classmethod
    def get_force_module_name(cls):
        return "全房间只打BOSS"

    def handle_receive(self, protocal_name: str, res: dict):
        if protocal_name.find("PushFruitBossShow") != -1:
            bossInfo = res["bossInfo"]
            bossSize = bossInfo["bossSize"]
            if bossSize == 3 or bossSize == 4:
                self.bossMap[bossInfo["index"]] = bossInfo

            now = time.time()
            for key, bossInfo in self.bossMap.items():
                if now >= bossInfo["createdTime"] + 100000:
                    del (self.bossMap[key])
        else:
            super().handle_receive(protocal_name, res)

"""
渔场加入1个陪玩机器人（1桌子1玩家1机器人）
"""
class OneRobotForceModule(AllRoomAllFishForceModule):
    def __init__(self, force_task_callback):
        super().__init__(force_task_callback)
        # 加入陪玩机器人数量
        self.count = 1

    @classmethod
    def get_force_module_name(cls):
        return "渔场加入1个陪玩机器人（1桌子1玩家1机器人）"

    # 设置陪玩机器人数量
    def _set_count(self, count):
        self.count = count

    def _do_before_test(self):
        if self.gold < 10000000000:
            self.add_command("ReqGiveMeItems", [{"1001": 10000000000, "1006": 100000000, "6001": 100000000, "6113": 100000000, "4001": 9999}, helper.KEY, self.playerId])
        if self.maxCannonMultiple < 500000:
            # 升级炮倍
            self.add_command("ReqOBUnlockCannonLv", [50000, True])
            time.sleep(1)
            # 切换到50000炮倍
            self.add_command("ReqFruitChangeMultiple", [50000])
        # 进房间 强制进入一个没人的桌子
        self.add_command("ReqEnterFruitRoom", [self.roomIndex, 1, 2])

    def handle_receive(self, protocal_name: str, res: dict):
        if protocal_name.find("ResEnterFruitRoom") != -1:
            self.tableId = res["info"]["tableId"]
            print(f" player: {self.playerId} 进入桌子 {self.tableId} 开始打鱼..")
            # 水果房间同步
            self.add_command("ReqFruitSynchGame", [])

            if self.count > 1:
                # 设置桌子位置上限数量
                param = f"SetFisheryTableSeatCount {self.roomIndex} 1 {self.tableId} {self.count}"
                self.add_command("ReqFruitConsole", [param])

            # 加入机器人命令
            param = f"RobotJoinTable {self.roomIndex} 1 {self.tableId} {self.count}"
            self.add_command("ReqFruitConsole", [param])

            self.isEnterRoom = True
        else:
            super().handle_receive(protocal_name, res)

"""
渔场加入多个陪玩机器人（1桌子1玩家N机器人）
"""
class ManyRobotForceModule(OneRobotForceModule):
    def __init__(self, force_task_callback):
        super().__init__(force_task_callback)
        # 加入陪玩机器人数量
        super()._set_count(10000)

    @classmethod
    def get_force_module_name(cls):
        return "渔场加入多个陪玩机器人（1桌子1玩家N机器人）"

"""
获取所有压测模块信息
"""
def get_all_force_module_info():
    # 获取当前模块对象
    current_module = inspect.currentframe().f_globals['__name__']
    module = __import__(current_module)

    # 获取当前模块中的所有成员
    all_members = inspect.getmembers(module)
    # 筛选出类对象
    classes = [member[1] for member in all_members if inspect.isclass(member[1])]

    res = ""
    # 打印所有类的名称
    for cls in classes:
        class_name = cls.__name__
        if not class_name.endswith("Module"):
            continue
        if class_name == "ForceModule":
            continue

        # 根据类名获取类对象
        class_obj = globals()[class_name]
        forceModuleName = class_obj.get_force_module_name()
        res += f"{forceModuleName}:{class_name};"

    return res


if __name__ == '__main__':
    helper.handle_dirty_players_config_data()
    # 开始压测
    task = ForceTask()
    task.start()
