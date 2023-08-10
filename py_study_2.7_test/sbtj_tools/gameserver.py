# coding:utf-8
from gameserveruse import *

task = Task("lz001", "1", ifCreateUser=True)  # playerId =
# task = Task("lz002", "1", ifCreateUser=True)  # playerId =
# task = Task("lz003", "1", ifCreateUser=True)  # playerId =
# task = Task("lz005", "1", ifCreateUser=True)  # playerId =
# task = Task("lz006", "1", ifCreateUser=True)  # playerId =
# task = Task("lz018", "1", ifCreateUser=True)  # playerId =
# task = Task("lz025", "1", ifCreateUser=True)  # playerId =
# task = Task("lz026", "1", ifCreateUser=True)  # playerId =

# task = Task("wqw1", "1", ifCreateUser=True)  # playerId =
# task = Task("wqw4", "1", ifCreateUser=True)  # playerId =

# task = Task("syj52", "1", ifCreateUser=True)  # playerId =
# task = Task("z9", "1", ifCreateUser=True)  # playerId =

# ----------------------------------------------------------------------------------->
# 查找:
# 1. 查找(sync@loadModule)module12: {"state":1,"data":{"0":{"12":
# 2. 推送(push@playerMoudle):       {"state":3,"data":{"player":{"1":{

# loadModule
# task.addCommand("sync@loadModule",{"module":"1"})

# 检查sdata更新
# task.addCommand("checkSdataUpdate", {})

# 解析GM指令
# task.addCommand("gm@gmcommand", {"cmd":"军官","param":"1"})
# task.addCommand("gm@gmcommand", {"cmd":"物品","param":"10000"})
# task.addCommand("gm@gmcommand", {"cmd":"道具","param":"90"})

# ----------------------------------------------------------------------------------->
# 军团指令 ------------------------------------------------>
# 获取军团指令信息
# task.addCommand("club@getClubOrderInfo", {})

# 发动指令
# task.addCommand("club@getClubOrderInfo", {"orderId":"", "param":""})

task.addCommand("unit@troopsGoHome", {})



task.start()