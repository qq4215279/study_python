# 动更辅助脚本

## 目的
对动更脚本执行进行封装

## 操作说明
**执行命令**：`python hotswap.py classNames="全限定类名" classesPath="字节码文件所在路径" attachProcessNames="附载程序名称"`

**参数说明**：

- **classNames**：需要被动更的全限定类名，多个类分号分割。eg：`com.cxx.hf.api.service.impl.activity.fisheryPlay.DragonBlessActivity`
- **classesPath**：上传到服务器的字节码文件所在目录路径，不传本地默认自动拷贝。eg：`DragonBlessActivity.class` 所在目录路径。

- **attachProcessNames**：需要被附载上的进程，不传本地默认附载 `game hall platform player` 4个游戏进程上。

eg：

- `python hotswap.py classNames=com.cxx.hf.api.service.impl.activity.fisheryPlay.DragonBlessActivity` 
- `python hotswap.py classNames=com.cxx.hf.api.service.impl.activity.fisheryPlay.DragonBlessActivity classesPath=C:\\Users\\D0381
  \\Desktop\\DragonBlessActivity.class attachProcessNames=com.cxx.hf.servergame.GameStart` 



## 测试服动更部署流程

1. 登录水果派 [工作台](http://172.16.12.243:8080/jenkins/)，进行测试服构建最新jar包。

2. 登录 [红桃运维管理平台](https://devops.yaojiyx.com/sgp_dev/server_action_dev/)。

   1. 选择 **水果派-测试服**  ->  **游戏动更**  页签。

   2. 输入需要被动更的 **全限定类名**。

   3. 选择需要被动更的 **附载进程**。

   4. 点击执行。

      **执行流程**：

      1. 拷贝被动更类字节码文件到服务器指定位置。
      2. 执行 `jar -jar game-agent.jar` 命令并输入指定参数。