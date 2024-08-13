# 刷新配置表  0: 服务器类型 1: 所有服务器; 3: hall; 4: game; 5: player; 6: platform    True: 测试服重新下载
# task.add_command("ReqRefreshConfigTable", [1, False])
# task.add_command("ReqRefreshConfigTable", [1, True])


# 获取功能状态  funcId
# task.add_command("ReqFunctionStatus", [500500])

# 请求给我发放一些道具
# task.send_msg_and_receive("ReqGiveMeItems", [{"1107": 1000}, helper.KEY, 10358])
# 加炮倍
# task.add_command("ReqOBUnlockCannonLv", [50000000])

# 请求玩家的邮件列表消息
# task.add_command("ReqMailList", [])

# 请求某个商店的具体内容
# task.add_command("ReqShopGoods", ["gold"])
# task.add_command("ReqShopGoods", ["stamps"])
# task.add_command("ReqShopGoods", ["monthcard"])

# 购买礼包 ================================================>
# 1. 购买钻石商城礼包
# task.buy_gift("diamond", 3000)
# 2. config_monthCard - 购买超值月卡
# task.buy_month_card(5003)
# 3. config_rechargePackage - 购买部落礼包1
# task.buy_charge_gift(10359)
# 4. config_shopMember - 购买30元贵族礼包
# task.buy_svip_card(20000)
# 5. config_shopGold - 购买5亿金币
# task.buy_gold_mail(2001)
# 6. config_shopStamps - 购买1点券
# task.buy_stamps_mail(12201)


# 荣耀盛典 ================================================>
# 0.1. 请求节日活动信息 festivalType = 40
# task.add_command("ReqFestivalInfo", [40])
# 0.2. 请求节日活动开启信息 有推送奖励调用
# task.add_command("ReqFestivalOpenInfo", [48])
# 1. 签到 activityId = 168
# 1.1.1 请求先到信息签到 activityId
# task.add_command("ReqHappySpringSign", [168])
# 1.1.2. 请求签到奖励  activityId
# task.add_command("ReqFestivalFreeReward", [168])
# 1.2.1. 请求圣诞签到页面信息  activityId
# task.add_command("ReqXmasSignInfo", [168])
# 1.2.2. 请求圣诞签到奖励  activityId  第几天
# task.add_command("ReqXmasSign", [168, 13])
# 2. 战令 activityId = 169
# 2.1. 战令信息:  activityId
# task.add_command("ReqFestivalGuideInfo", [169])
# 2.2. 领取战令奖励 activityId  guideType  等级
# task.add_command("ReqFestivalGuideReward", [169, 0, 1])
# 3. 盛典赏金 activityId = 170
# 3.1. 请求获取盛典赏金界面信息 activityId
# task.add_command("ReqGetCeremonyBountyBasicInfo", [170])
# 3.2. 请求获取盛典赏金信息 activityId  floor
# task.add_command("ReqGetCeremonyBountyInfo", [170, 1])
# 3.3. 请求获取盛典赏金界面信息 activityId  floor  choosePosition
# task.add_command("ReqDrawCeremonyBounty", [170, 1, 1])
# 4. 活动任务 activityId = 171
# 4.1. 请求节日通用任务信息 activityId
# task.add_command("ReqCommFestivalTaskInfo", [171])
# 4.2. 请求通用节日活动任务奖励 activityId  taskId列表
# task.add_command("ReqCommFestivalTaskReward", [171, 1])
# 5. 活动礼包 activityId = 172
# 5. 请求节日活动礼包信息 activityId
# task.add_command("ReqFestivalShopInfo", [172])


# 粽情端午 ================================================>
# 0. 请求节日活动信息 festivalType = 48
# task.add_command("ReqFestivalInfo", [48])
# 请求节日活动开启信息 有推送奖励调用
# task.add_command("ReqFestivalOpenInfo", [48])

# 1. 签到 activityId = 194
# 1.1. 请求签到页面信息  activityId
# task.add_command("ReqXmasSignInfo", [194])
# 1.2. 请求节日活动任务信息
# task.add_command("ReqFestivalTaskInfo", [194])
# 1.3. 请求签到奖励  activityId  第几天
# task.add_command("ReqXmasSign", [194, 1])

# 2. 战令  activityId = 195
# 2.1. 战令信息:  activityId = 195
# task.add_command("ReqFestivalGuideInfo", [195])
# 2.2. 领取战令奖励 activityId  guideType  等级
# task.add_command("ReqFestivalGuideReward", [195, 0, 1])

# 3. 包粽子 activityId = 196
# 3.1. 请求节日兑换页面信息
# task.add_command("ReqFestivalExchangeInfo", [196])
# 3.2. 请求节日兑换  activityId  exchangeId  times
# task.add_command("ReqFestivalExchange", [196, 129, 1])
# task.add_command("ReqFestivalCommExchange", [196, 129, 1])

# 4. 抽奖 activityId = 197
# 4.1. 请求抽奖多类型信息 activityId
# task.add_command("ReqFestivalMultipleDrawInfo", [197])
# 4.2. 请求抽奖 activityId  times: 抽奖次数  drawType: 抽奖类型
# task.add_command("ReqFestivalDraw", [197, 10, 0])

# 5. 限时折扣 activityId = 198
# 5.1. 请求节日打鱼福利礼包
# task.add_command("ReqFestivalFishingWelfareGift", [198])
# task.add_command("ReqFestivalMulFishingWelfareGift", [198])

# 6. 端午勋章 activityId = 199
# 6.1. 请求获取节日活动勋章信息  activityId
# task.add_command("ReqGetFestivalMedalInfo", [199])
# 6.2. 请求节日活动任务信息  activityId
# task.add_command("ReqFestivalTaskInfo", [199])
# 6.3. 请求激活节日活动勋章等级
# task.add_command("ReqActivateFestivalMedalLevel", [199])
# 6.4. 请求勋章信息
# task.add_command("ReqMedalInfo", [-1])

# 7. 端午特惠 activityId = 200
# task.add_command("ReqFestivalShopInfo", [200])


# 夏日盛典 ================================================>
# 0. 请求节日活动信息 festivalType = 51
# task.add_command("ReqFestivalInfo", [52])

# task.add_command("ReqFestivalInfo", [48])

# 1. 夏日签到 activityId = 204
# 1.1. 请求签到页面信息  activityId
# task.add_command("ReqXmasSignInfo", [204])
# 1.2. 请求节日活动任务信息
# task.add_command("ReqFestivalTaskInfo", [204])
# 1.3. 请求签到奖励  activityId  第几天
# task.add_command("ReqXmasSign", [204, 1])

# 3. XXX礼包 activityId = 205
# task.add_command("ReqFestivalShopInfo", [205])

# 4. 疯狂水战 activityId = 206
# 4.1. 请求获取节日怪物信息  activityId
# task.add_command("ReqGetFestivalWaterMonsterInfo", [206])
# 4.2. 请求攻击节日怪物  activityId  consumeItemId 消耗道具id  times 攻击次数
# task.add_command("ReqHitFestivalWaterMonster", [206, 3590, 1])

# 5. 夏日礼包 activityId = 207
# task.add_command("ReqFestivalShopInfo", [207])

# 6. 夏日勋章 activityId = 208
# 6.1. 请求获取节日活动勋章信息  activityId
# task.add_command("ReqGetFestivalMedalInfo", [208])
# 6.2. 请求节日活动任务信息  activityId
# task.add_command("ReqFestivalTaskInfo", [208])
# 6.3. 请求激活节日活动勋章等级
# task.add_command("ReqActivateFestivalMedalLevel", [208])
# 6.4. 请求勋章信息
# task.add_command("ReqMedalInfo", [-1])