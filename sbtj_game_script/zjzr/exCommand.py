#coding:utf-8
from conn2server import *
from jinja2 import *
import json

# 填充模板参数
task = Task("lz003", "1", u"标题")

task.connect2Server()

task.excuseWithRtn("player@getPlayerInfo",{"playerId":"11809","age":"19","aesType":"1"})

# task.excuseWithRtn("pay@createPayOrder",{"itemId":"10","type":"1"})


# task.excuseWithRtn("explore@getExploreTicketShopInfo",{"gameState":"0","formationType":"1","args":"20;20001"})


task.buildMDDoc("mdDOC.template")
task.close()