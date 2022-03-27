# coding=utf-8

import json
import random
from map_util import *

'''
默认回调
'''
def default_call_back(api_result, content):
    for index, state in enumerate(content.states):
        if state == 1:
            pass
        else:
            content.states[index] = 1
            return


'''
测试上限文
'''
class Content:

    def __init__(self):
        pass

    # 编队列表
    troops = []
    # 是否可以执行这个请求
    states = []
    # 主城点
    main_city_reference_point = 0


'''
请求包装类
'''
class RequestWrapper:
    # 请求上下文
    content = None

    def __init__(self, content):
        self.content = content
        pass

    '''
    请求后的回调
    '''
    def after_call(self, result):
        pass

    '''
    请求前的回调
    '''
    def before_call(self, param):
        return param


'''
部队数据
'''
class TroopArrayWrapper(RequestWrapper):

    def after_call(self, result):
        res = json.loads(result)
        self.content.troops = res["data"]["group"]


'''
玩家主城中心点
'''
class PlayerCityReferencePointWrapper(RequestWrapper):

    def after_call(self, result):
        res = json.loads(result)
        self.content.main_city_reference_point = res["data"]["index"]


'''
行军
'''
class MoveWrapper(RequestWrapper):

    def before_call(self, param):
        x, y = index_to_x_y(self.content.main_city_reference_point)
        # 随机的x
        random_x = random.randint(-100, 100) + x
        # 随机的y
        random_y = random.randint(-100, 100) + y
        # 随机一个部队
        random_index = random.randint(0, 2)
        ids = str(self.content.troops[random_index]["groupUniqueId"])
        return {"x": "" + str(random_x), "y": "" + str(random_y), "groupUniqueIds": "" + ids}
