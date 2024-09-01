# encoding: utf-8

import gzip
import os
import sys
from datetime import datetime, date


# 被分析日志文件所在目录
# LOG_DIRECTORY = "/data/logs"
LOG_DIRECTORY = "E:\\Data\\logs\\SG"
# 目标游戏服务
TARGETS = {"game1", "game2", "hall1", "hall2", "platform1", "platform2", "player1", "player2"}

# playerId 与 itemOb列表 映射
ITEM_OB_DICT = {}

"""
道具日志对象
"""
class Item:
    def __init__(self, timeStr, fromFile, playerId, itemId, count, curCount, circType) -> None:
        self.timeStr = timeStr
        self.fromFile = fromFile
        self.playerId = playerId
        self.itemId = itemId
        self.count = count
        self.curCount = curCount
        self.circType = circType

        self.timestamp = self.__get_timestamp(timeStr)

    # 排序
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __get_timestamp(self, timeStr) -> int:
        # 定义时间字符串的格式
        format_str = "%Y-%m-%d at %H:%M:%S.%f"
        # 将字符串转换为时间对象
        dt = datetime.strptime(timeStr, format_str)
        return dt.timestamp() * 1000

    def getWriteLine(self):
        return f"time: {self.timeStr}, fromFile: {self.fromFile}, playerId: {self.playerId}, itemId: {self.itemId}, count: {self.count}, " \
               f"curCount: {self.curCount}, circType: {self.circType}\n"


"""
分析道具日志
"""
def analysis_item_log(year: int, month: int, day: int):
    parse_directory(year, month, day)
    analysis_items()


"""
1. 解析指定日期道具日志文件
"""
def parse_directory(year: int, month: int, day: int):
    arr = __parse_file_name(year, month, day)
    isToday = arr[0]
    suffix_file = arr[1]

    for target in TARGETS:
        path = f"{LOG_DIRECTORY}/{target}/{suffix_file}"
        print("path: ", path)
        if not os.path.exists(path):
            continue
        __parse_single_file(target, isToday, path)

# 解析文件名称
def __parse_file_name(year: int, month: int, day: int):
    targetDT = date(year, month, day)

    isToday = True
    # 当天日志
    if targetDT == date.today():
        suffix_file = "ItemCircLogger.log"
    else:
        isToday = False

        monthStr = str(month)
        daStr = str(day)
        if month < 10:
            monthStr = "0" + monthStr
        if day < 10:
            daStr = "0" + daStr
        suffix_file = f"{year}-{monthStr}/ItemCirc-{year}-{monthStr}-{daStr}-1.log.gz"

    return isToday, suffix_file

# 解析单个文件
def __parse_single_file(target, isToday, path):
    # 解析gz压缩文件
    if not isToday:
        with gzip.open(path, 'r') as file:
            for line in file.readlines():
                __parse_line_log(line, target)
    else:
        with open(path, "r", encoding="utf-8") as file:
            for line in file.readlines():
                __parse_line_log(line, target)

# 解析单行日志
def __parse_line_log(line, target):
    # if is_binary(line):
    #     line = line.decode(encoding='utf-8')
    line = decode_binary_line(line)

    # TODO 指定道具为金币 1001
    key = "itemId=1001"
    if line.find(key) == -1:
        return

    itemOb = __general_Item(line, target)
    if itemOb.playerId not in ITEM_OB_DICT:
        ITEM_OB_DICT[itemOb.playerId] = list()
    ITEM_OB_DICT[itemOb.playerId].append(itemOb)

# 解码二进制行信息
def decode_binary_line(line):
    try:
        return line.decode('utf-8')
    except AttributeError:
        return line

# 解析行日志生成 ItemOb 对象
def __general_Item(line: str, fileName: str) -> Item:
    lineArr1 = line.split(" CST - ")
    timeStr = lineArr1[0]

    comma = "…_…"
    if line.find("\xe2\x80\xa6_\xe2\x80\xa6") != -1:
        comma = "\xe2\x80\xa6_\xe2\x80\xa6"

    infoArr = lineArr1[1].split(comma)
    playerId = int(infoArr[0].split("=")[1])
    itemId = int(infoArr[1].split("=")[1])
    count = int(infoArr[2].split("=")[1])
    curCount = int(infoArr[3].split("=")[1])
    circType = infoArr[4].split("=")[1]
    return Item(timeStr, fileName, playerId, itemId, count, curCount, circType)


"""
2. 分析日志
"""
def analysis_items():
    # 当前工作目录
    directory = os.path.dirname(__file__)
    # 1. 删除上一次工作目录
    errorPlayerPath = f"./errorPlayers"
    __delete_old_files(errorPlayerPath)

    # 2. 解析玩家
    for playerId, itemOB_list in ITEM_OB_DICT.items():
        itemOB_list = sorted(itemOB_list, key=lambda ob: ob.timestamp)

        rewrite_list = list()
        needReWrite = False

        length = len(itemOB_list)
        for i in range(length):
            itemOb = itemOB_list[i]
            rewrite_list.append(itemOb.getWriteLine())

            if i + 1 >= length:
                break

            nextItemOb = itemOB_list[i + 1]
            # 出现异常数据！！！
            if itemOb.curCount + nextItemOb.count != nextItemOb.curCount:
                needReWrite = True
                rewrite_list.append("出现异常数据---------------->\n")
                rewrite_list.append("\n")
                rewrite_list.append("后续日志数据---------------->\n")
                rewrite_list.append(nextItemOb.getWriteLine())
                if i + 2 < length - 1:
                    rewrite_list.append(itemOB_list[i + 2].getWriteLine())
                if i + 3 < length - 1:
                    rewrite_list.append(itemOB_list[i + 3].getWriteLine())
                if i + 4 < length - 4:
                    rewrite_list.append(itemOB_list[i + 4].getWriteLine())
                break


        if needReWrite:
            __write_error_player(f"{errorPlayerPath}/{playerId}.txt", rewrite_list)

# 将日志有错误的玩家记录到文件中
def __write_error_player(path, rewrite_list):
    print("write error player path: ", path)
    with open(path, "w", encoding="utf-8") as file:
        for str in rewrite_list:
            file.write(str)

# 创建目录并删除上一次分析数据
def __delete_old_files(errorPlayerPath):
    if not os.path.exists(errorPlayerPath):
        os.makedirs(errorPlayerPath)
        return

    for file_name in os.listdir(errorPlayerPath):
        try:
            path = f"{errorPlayerPath}/{file_name}"
            if os.path.isfile(path):
                os.remove(path)
        except Exception as e:
            print(f"Error occurred while deleting file: {file_name}")
            print(f"Error message: {e}")


"""
获取参数信息
"""
def get_args():
    year = 2024
    month = 1
    day = 17
    for arg in sys.argv:
        if arg.find("=") == -1:
            continue

        arr = arg.split("=")
        i = int(arr[1])
        if arr[0] == 'year':
            year = i
        if arr[0] == 'month':
            month = i
        if arr[0] == 'day':
            day = i

    return year, month, day


if __name__ == '__main__':
    args = get_args()
    year = args[0]
    month = args[1]
    day = args[2]

    """
    使用步骤:
        1. 修改变量修改本地日志文件所在目录，操作当前文件如下变量: LOG_DIRECTORY
        2. 执行命令：
            2.1. 本地环境执行命令: python item_analysis_linux.py year=2024 month=1 day=19
            2.2. 如果是在测试服，则执行如下命令: python3.8 item_analysis_linux.py year=2024 month=1 day=19
            注：year指定年(默认可不填)，month指定月份，day指定日期
        3. 结果查看: 若有玩家道具日志异常，会在如下目录下生成对应玩家道具日志信息: hf-parent\\3rd-party\\py_tools\\log_analysis\\errorPlayers\\
    """
    analysis_item_log(year, month, day)
