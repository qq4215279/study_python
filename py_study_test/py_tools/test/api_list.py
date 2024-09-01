# 刷新配置表  0: 服务器类型 1: 所有服务器; 3: hall; 4: game; 5: player; 6: platform    True: 测试服重新下载
# task.add_command("ReqRefreshConfigTable", [1, False])
# task.add_command("ReqRefreshConfigTable", [1, True])

# 控制台命令
# 设置桌子位置上限数量
param = f"SetFisheryTableSeatCount 1 1 1 5"
# task.add_command("ReqFruitConsole", [param])
# 加入机器人命令
param = f"RobotJoinTable 1 1 1 1"
# task.add_command("ReqFruitConsole", [param])

# 请求冻结玩家账号  type 冻结状态: 0: 解除冻结; 1: 冻结   playerId
# task.add_command("ReqFreezePlayer", [1, 10432])
# 请求清除玩家缓存  playerId
# task.add_command("ReqClearPlayerCache", [10432])

# 获取功能状态  funcId
# task.add_command("ReqFunctionStatus", [500500])

# 客户端请求某个商店的具体内容  funcId
# task.add_command("ReqShopGoods", [180800])

# 请求给我发放一些道具
# task.send_msg_and_receive("ReqGiveMeItems", [{"1107": 1000}, helper.KEY, 10358])


# 战令test ---------------------------------------------------------------------->
# 1. 获取战令信息
# task.add_command("ReqGetPlayerWarOrderInfo", [])
# 2. 请求领取战令通行证奖励
# task.add_command("ReqGetWarOrderPassCardReward", [])
# 3. 请求获取夏日寻访信息
# task.add_command("ReqGetSummerTourInfo", [])
# 4. 请求寻访  寻访类型: 1: 阳光海滩; 2: 泳池派对    次数
# task.add_command("ReqDrawSummerTour", [1, 1])
# 5. 请求领取寻访额外奖励  寻访类型: 1: 阳光海滩; 2: 泳池派对   序列
# task.add_command("ReqGetSummerTourExtraReward", [1, 1])
# 6. 请求获取夏日探宝信息
# task.add_command("ReqGetSummerTreasureInfo", [])
# 7. 请求夏日探宝  探宝类型: 1: 免费; 2: 普通; 3: 高级   探宝次数
# task.add_command("ReqDrawSummerTreasure", [1, 1])
# 8. 请求领取夏日探宝累计任务奖励  需要累计探宝次数
# task.add_command("ReqGetTreasureCumulateTaskReward", [4])
# 9. 请求获取战令任务信息
# task.add_command("ReqGetWarOrderTaskInfo", [])
# 10. 请求领取战令任务奖励  任务id: >0: 具体任务; -1: 每日任务可领奖列表; -2: 每周任务可领奖列表; -3: 每期任务可领奖列表
# task.add_command("ReqGetWarOrderTaskReward", [-1000])


# 1. 请求关注公众号福利
# task.send_msg_and_receive("ReqFollowWeChat", [])
# 2. 兑换公众号奖励  微信id 玩家id  消息内容 类型
# ExchangeActionServlet  ->  doPost  ->  ReqAdminWechatText
# task.send_msg_and_receive("ReqAdminWechatTextMessage", [])
