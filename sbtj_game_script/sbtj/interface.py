
# loadModule
# task.addCommand("sync@loadModule",{"module":"chatSend"})
# task.addCommand("sync@loadModule",{"module":"3"})

# ---------------------------------->

# 1.1发送私聊
# task.addCommand("chat@send", {"target":"2", "msg":"q002发送私聊99999"})
# task.addCommand("chat@send", {"target":"1", "msg":"q002发送私聊999999999998"})
# task.addCommand("chat@send", {"target":"1", "msg":"q002发送私聊979776"})

# 1.2获得私聊
# task.addCommand("chat@getChatCacheInfo", {"target":"2"})
# task.addCommand("player@getChatCacheInfo", {})

# 2.1向全服发送系统消息
# task.addCommand("chat@sendGlobal", {"msg":"全服发送消息2222"})
# 2.2获取
# task.addCommand("chat@getGlobalChatCacheInfo", {})

# 3.1向所在州发送消息
# task.addCommand("chat@sendRegion", {"msg":"向所在州发送消息111111"})
# task.addCommand("chat@sendRegion", {"msg":"向所在州发送消息22222"})
# 3.2获取
# task.addCommand("chat@getRegionChatCacheInfo", {})

# 4.1发送同盟聊天
# task.addCommand("chat@sendClub",{"msg":"啊啊啊啊啊啊啊444444"})
# 4.2获取同盟聊天信息
# task.addCommand("chat@getClubChatCacheInfo",{})

# 5.1发送群组聊天
# task.addCommand("chat@sendGroup",{"groupId":"31","msg":"群组31聊天999"})
# 5.2获取群组聊天信息
# task.addCommand("chat@getGroupChatCacheInfo",{"groupId":"1"})

# 6.向全服发送系统消息
# task.addCommand("chat@sendSystemMsgToAll", {"msg":"向全服发送系统消息"})

# 7.向个人发送系统消息
# task.addCommand("chat@sendSystemMsg", {"playerId":"4","msg":"向个人发送系统消息"})

# 8.获取系统发送给个人聊天信息
# task.addCommand("chat@getSystemMsg", {})

# ------------------------------------------------------------------------------->
# 好友
# 1.申请
# task.addCommand("friend@apply", {"friendId": "1", "playerName": ""})
# task.addCommand("friend@apply",{"friendId":"","playerName":"test003"})

# 2. 申请列表
# task.addCommand("friend@getApplyList",{})

# 3.1接受
# task.addCommand("friend@acceptApply",{"targetPlayerId":"2"})
# 3.2
# task.addCommand("friend@acceptTotalApply",{})

# 4. 清空申请列表
# task.addCommand("friend@clearApply",{})

# 5. 删除好友
# task.addCommand("friend@deleteFriend",{"targetPlayerId":"4"})

# 6. 加入黑名单
# task.addCommand("friend@addBlackList",{"targetPlayerId":"10"})

# 5. 移除黑名单
# task.addCommand("friend@removeBlackList",{"targetPlayerId":"7"})

# 6. 获取好友列表
# task.addCommand("friend@getFriendList",{})

# 7. 获取黑名单列表
# task.addCommand("friend@getBlackList",{})

# 8. 获取玩家信息信息
# task.addCommand("friend@getPlayerMsg",{"otherPlayerId":"4"})


# 群组
# 1.创建群组
# task.addCommand("sbtj@create",{"name":"q001群组","friendIds":"2,3"})

# 2.邀请加入群组
# task.addCommand("sbtj@invite",{"groupId":"2","friendIds":"1"})

# 3.1接收邀请
# task.addCommand("sbtj@acceptInvite",{"groupId":"19"})

# 3.2 一键接受所有邀请
# task.addCommand("sbtj@oneClickAccept",{})

# 4.拒绝邀请
# task.addCommand("sbtj@refuseInvite",{"groupId":"2"})

# 5.清空邀请列表
# task.addCommand("sbtj@clearInvite",{})

# 6.开启免打扰
# task.addCommand("sbtj@openNobother",{"groupId":"1"})

# 7.关闭免打扰
# task.addCommand("sbtj@closeNobother",{"groupId":"1"})

# 8.踢除群组成员
# task.addCommand("sbtj@removeMember",{"groupId":"2","target":"1"})

# 9.退出群组（群主退出则解散群组）
# task.addCommand("sbtj@exitGroup",{"groupId":"31"})

# 10.获取群组列表
# task.addCommand("sbtj@getGroupList",{})

# 11.获取当前群组成员列表
# task.addCommand("sbtj@getMemberList",{"groupId":"1"})

# 12. 获取邀请列表
# task.addCommand("sbtj@getInviteList",{})

# task.addCommand("chat@test",{})

# 友盟 ----------------------->
# 1. 申请添加友盟
# task.addCommand("club@applyUnion", {"clubId":"2"})

# 2. 获取同盟申请列表
# task.addCommand("club@getUnionApplyList", {})

# 3. 接受同盟申请
# task.addCommand("club@acceptUnionApply", {"clubId":"4"})

# 4. 拒绝同盟申请
# task.addCommand("club@refuseUnionApply", {"clubId":"4"})

# 5.清空同盟申请列表
# task.addCommand("club@clearUnionApply", {})

# 6.解除友盟
# task.addCommand("club@removeUnion",{"clubId": "1"})

# 7.获取友盟列表
# task.addCommand("club@getUnionList", {})

# 8. 获取同盟列表
# task.addCommand("club@getClubList", {})

# 1. 获取升星条件
# task.addCommand("unit@increaseStarCondition", {"playerUnitId":"563"})

# 2. 升星
# task.addCommand("unit@increaseStar", {"playerUnitId":"536","playerUnitIds":"544,552"})

# 3. 获取可升星武将
# task.addCommand("unit@redPointsMsg", {})
# task.addCommand("unit@redPointsMsgByPlayerUnitId", {"playerUnitId":"563"})

# 4. 重塑
# task.addCommand("unit@reset", {"playerUnitId":"506"})

# 5. 预览重塑
# task.addCommand("unit@previewReset", {"playerUnitId":"506"})

# 6. 拆解预览
# task.addCommand("unit@previewDisassembly", {"playerUnitIds":"4,5"})

# 7. 拆解
# task.addCommand("unit@disassembly", {"playerUnitIds":"767,511"})

# ------------------->
# 私聊开启消息免打扰
# task.addCommand("friend@openNoBotherMsg", {"friendId": "3"})

# 私聊关闭消息免打扰
# task.addCommand("friend@closeNoBotherMsg", {"friendId": "1"})

# 使用军令道具
# task.addCommand("player@useWarTokenProp", {"count":"1"})
# task.addCommand("sync@loadModule",{"module":"10"})
# 购买战令
# task.addCommand("player@buyWarToken", {"count":"1"})

# 通过名字找玩家
# task.addCommand("player@getPlayer", {"name":"q001"})

# 联系人信息
# task.addCommand("player@contactsMsg", {})

# 获取正在研究的科技信息
# task.addCommand("science@getCreatingMsg", {"cityNo":"0"})

# 获取资源信息
# task.addCommand("science@getResourceMsg", {})

# 领取资源
# task.addCommand("player@receiveResource", {})
# 获取
# task.addCommand("science@getResourceMsg", {})

# 使用道具
# task.addCommand("bag@useProp", {"props":"28:1:10"})

# 运输 --------------------------->
# 获取运输信息
# task.addCommand("transport@getInfo", {})

# 开始运输（呼叫空运）
# task.addCommand("transport@startTransport", {"nums":"120000:0:0"})

# 终止运输运输（紧急起飞）
# task.addCommand("transport@stopTransport", {})

# 领取运输资源
# task.addCommand("transport@getResource", {})

# 购买资源道具（军费、钢铁、石油）并使用
# task.addCommand("bag@buyResourceProp", {"prop":"28:1:2"})

# 购买指定数量资源（军费、钢铁、石油）
# task.addCommand("bag@buyResource", {"type":"1","nums":"10000"})

# task.addCommand("sync@loadModule",{"module":"5"})

# 开始征兵
# task.addCommand("player@summonFire", {"num":"2"})

# 停止征兵
# task.addCommand("player@stopSummonFire", {})

# 武将加经验
# task.addCommand("unit@addExp", {"playerUnitId":"180","num":"10"})

# 迁城
# task.addCommand("world@moveCity", {"index":"643532"})

# 驻防友军主城
# task.addCommand("world@defendFriendCity", {"index":"602880", "groupUniqueIds":"82"})

# 取消驻防友军主城
# task.addCommand("world@cancelDefendFriendCity", {"groupUniqueIds":"82"})

# 军团 ------------------------>
# 搜索军团
# task.addCommand("club@searchClub", {"keyword":"A"})

# 搜索玩家
# task.addCommand("player@searchPlayer", {"keyword":"z22"})

# 军团商店商品数据
# task.addCommand("club@getShopInfo", {})

# 军团商店商品数据
# task.addCommand("club@buy", {"index":"1","num":"1"})

# 军团互助 --------------------->
# 请求科技研究加速 sciTypes: 科技type；个用“,” 隔开
# task.addCommand("club@askScienceHelp", {"sciTypes":"102"})

# 请求维修基地
# task.addCommand("club@askFixPlayerCity", {})

# 获取请求互助列表
# task.addCommand("club@getHelpList", {})

# 帮助军团盟友
# task.addCommand("club@helpClubMembers", {})

# 军团科技 --------------------->
# 获取军团科技信息
# task.addCommand("club@getSciInfo", {})

# 获取军团科技信息
# task.addCommand("club@getSciInfoByType", {"type":"100"})

# 捐献军团科技点
# task.addCommand("club@donateSciPoint", {"type":"100","method":"2"})

# 推荐捐献科技
# task.addCommand("club@recommendSci", {"type":"100"})

# 升级军团科技
# task.addCommand("club@upgradeSci", {"type":"100"})

# 获取正在研究的科技信息
# task.addCommand("club@getCreatingMsg", {})

# 获取军团战略要地信息
# task.addCommand("club@getStrategyAreasInfo", {})

# 军团邮件 ---------------------->
# 根据起始和结束获得玩家邮件信息
# task.addCommand("mail@getAllMail", {"tag":"1"})

# 一键阅读并领取奖励
# task.addCommand("mail@readAndRecieveAll", {"tag":"1"})

# 调度中心 ---------------------->
# 获取调度中心信息
# task.addCommand("club@getTradeInfo", {})

# 提供
# task.addCommand("club@provide", {"gold":"100","iron":"100","fossilOil":"100"})

# 获取
# task.addCommand("club@get", {"gold":"100","iron":"100","fossilOil":"100"})

# 捐赠资源（用于司令部建造）
# task.addCommand("club@donateResource", {"gold":"100000","iron":"1000000","fossilOil":"200000"})

# 获取军团战略部署信息
# task.addCommand("club@getStrategyMapsInfo", {})

# 捐赠资源（用于司令部建造）
# task.addCommand("player@getBattleInfo", {"targetPlayerId":"6"})

# 获取军功商店信息
# task.addCommand("player@getMilitaryShopInfo", {})

# 购买军功商店商品
# task.addCommand("player@buy", {"index":"1", "num":"1"})

# 获取军团任务列表
# task.addCommand("club@getClubTasksInfo", {})

# 获取军团任务列表
# task.addCommand("club@doneTask", {"taskId":""})

# 一键升星预览（一键研发预览）
# task.addCommand("unit@previewQuickIncreaseStar", {})

# 一键升星（一键研发）
# task.addCommand("unit@quickIncreaseStar", {"playerUnitIds": "1771;1777","consumePlayerUnitIds": "2995,3019,1671,1643,1022;2996,3020,1691,1741,1711"})

# -------------------------------------------------------------------------------->
# 获取支线任务info
# task.addCommand("task@getBranchTasksInfo", {"headId":"1"})

# 领取支线任务奖励
# task.addCommand("task@getReward", {"taskId":"205005"})

# 获取支线任务主题信息
# task.addCommand("task@getBranchTopicInfo", {})

# ========================>
# 获取玩家军衔信息
# task.addCommand("player@getPlayerMilitaryRankInfo", {})

# 获取指定军衔信息
# task.addCommand("player@getMilitaryRankInfo", {"militaryRank":"5"})

# 进阶军衔
# task.addCommand("player@addMilitaryRank", {})

# 获取军衔进阶奖励
# task.addCommand("player@getMilitaryRankReward", {})

# 获取军衔每日奖励
# task.addCommand("player@getMilitaryRankDailyReward", {})

# ========================>
# 获取玩家战力排行榜
# task.addCommand("rank@getBattlePointRank", {})

# 获取玩家军衔积分排行榜
# task.addCommand("rank@getMilitaryScoreRank", {})

# 获取军团玩家总战力值排行榜
# task.addCommand("rank@getClubBattlePointRank", {})

# 获取军团玩家军衔总军衔积分排行榜
# task.addCommand("rank@getClubMilitaryRank", {})

# 获取军功商店信息
# task.addCommand("player@getMilitaryShopInfo", {})

# 购买军功商店商品
# task.addCommand("player@buy", {"index":"1", "num":"1"})

# 军团进阶 ------------------------------------------------>
# 获取军团信息
# task.addCommand("club@getInfo", {"clubId":"8"})

# 获取军团进阶条件信息
# task.addCommand("club@getClubAdvanceInfo", {})

# 开始进阶
# task.addCommand("club@startClubAdvance", {"index":"680845"})
# task.addCommand("structure@getInfo", {"type":"2"})

# 军官系统 ------------------------------------------------>
# 1. 获取军官列表
# task.addCommand("commander@getCommanderList", {})

# 1. 获取自己拥有的军官列表
# task.addCommand("commander@getSelfCommanderList", {})

# 2. 获取军官信息
# task.addCommand("commander@getCommanderInfo", {"commanderId":"100800"})

# 3. 使用军官经验书增加经验 props: dropType:goodsId:num;dropType:goodsId:num
# task.addCommand("commander@addCommanderExp", {"commanderId":"100100","props":"42:1:1;42:2:1"})

# 4. 获取指挥官技能列表
# task.addCommand("commander@getCommanderSkillList", {})

# 5. 学习指挥官技能
# task.addCommand("commander@studyCommanderSkill", {"commanderId":"100100","playerCommanderSkillId":"9"})

# 6. 升级指挥官技能
# task.addCommand("commander@upgrader@getCommanderInfoCommanderSkill", {"playerCommanderSkillId":"9"})

# 7. 重置指挥官技能
# task.addCommand("commander@resetCommanderSkill", {"playerCommanderSkillId":"9"})

# 8. 军官上阵
# task.addCommand("commander@addToGroup", {"commanderId":"100100","groupId":"1"})

# 9. 军官下阵
# task.addCommand("commander@removeFromGroup", {"commanderId":"100100"})


# 抽卡商店 ------------------------------------------------>
# 1. 抽卡商店商品数据
# task.addCommand("explore@getShopInfo", {})

# 2. 商品购买
# task.addCommand("explore@buy", {"index":"1","num":"1"})

# 购买军功商店商品
# task.addCommand("player@buy", {"goodsId":"1", "num":"1"})