#coding:utf-8
from gameserveruse import *

task = Task("熊仔", "1", ifCreateUser = True)

#task.addCommand("gm@gmcommand", {"cmd":"功能","param":"7"})


# 活跃
#  task.addCommand("activity@getInfo", {"activityId":"90"})

# 充值
#task.addCommand("activity@getInfo", {"activityId":"91"})

# 兑换
# task.addCommand("activity@getInfo", {"activityId":"92"})

#task.addCommand("backstage@genCeHuaJSON", {})

# 获取标签页下有哪些建筑
#task.addCommand("structure@getTabInfo", {"tab":"1"})

# 获取这个建筑的信息
#task.addCommand("structure@getInfo", {"type":"1"})

# 升级这个建筑
#task.addCommand("structure@lvUp", {"type":"1"})

# 建筑升级秒cd
#task.addCommand("structure@clearLvUpCD", {"type":"1"})

#task.addCommand("user@login",{"username":"王者","password":"1","platform":"1","serverId":"1"})

#task.addCommand("user@createUser",{"username":"王者2","password":"1"})



# UserTest 接口
#task.addCommand("userTest@getCurrentTimeMills",{})

# 注册
#task.addCommand("createUser",{"userName":"mumu5","password":"123"})

# 登录
#task.addCommand("login",{"userName":"mumu5","password":"123"})

# 激活用户
#task.addCommand("activeUser",{"idCard":"360728200004211314","age":"20","phone":"18279719822"})

# 进入副本 
#task.addCommand("play@intoCopy",{"chapterId":"1"})
#task.addCommand("play@getChapterInfo",{"chapterId":"1"})

# 进入据点
#task.addCommand("play@intoStage",{"stageId":"1"})
#task.addCommand("play@enterStage",{"stageId":"1"})

# 挑战据点
#task.addCommand("play@startStage",{"stageId":"1"})
#task.addCommand("play@sweepStage",{"stageId":"6"})

# 10连扫
#task.addCommand("play@tenSweepStage0",{"stageId":"1"})
#task.addCommand("play@tenSweepStage",{"stageId":"4"})

# 强攻
#task.addCommand("play@stormStage0",{"stageId":"1"})
#task.addCommand("play@stormStage",{"stageId":"1"})

# ------------------------------------------------------------->

# 获取排位信息
#task.addCommand("rank@getInfo",{})

# 挑战排位赛
#task.addCommand("rank@challenge",{"opponentId":"1"})

# 购买冷却缩减
#task.addCommand("rank@buyCutCD",{})

# 购买挑战次数
#task.addCommand("rank@buyRankTimes",{})

# 排位赛排行榜
#task.addCommand("rank@getRankInfoList",{})

task.addCommand("chat@send", {"msgType":"1", "target":"2", "msg":"sssddd", "param":"sss"})


task.start()
task.close()
