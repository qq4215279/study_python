# encoding: utf-8

from datetime import datetime, date, time, timedelta

"""
datetime包：处理日期和时间的类和函数，用于执行各种与日期和时间相关的操作。以下是该模块中一些主要的类：

1. datetime 类：最常用的日期时间类，包含了年、月、日、时、分、秒以及微秒。你可以使用它表示一个特定的日期和时间。
    1.1. dt = datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]): 创建一个 datetime 对象，表示给定的日期和时间。
        参数的含义分别是年、月、日、时、分、秒、微秒、时区。eg: dt = datetime(2023, 7, 4, 12, 30, 45, 100)
        1.1.1. 属性获取：
            dt.year: 年份
            dt.month: 月份（1 到 12）
            dt.day: 日
            dt.hour: 小时（0 到 23）
            dt.minute: 分钟（0 到 59）
            dt.second: 秒（0 到 59）
            dt.microsecond: 微秒
            dt.tzinfo: 时区信息
        1.1.2. dt.strftime()  将 datetime 对象格式化为字符串    
            常用的格式化字符串: eg: print(dt.strftime("%Y-%m-%d %H:%M"))
                %Y: 年（四位数）
                %m: 月（01 到 12）
                %d: 日（01 到 31）
                %H: 小时（00 到 23）
                %M: 分钟（00 到 59）
                %S: 秒（00 到 59）
                %f: 微秒
        1.1.3. dt.timestamp()  将datetime对象转为秒。此返回值是与 time.time() 返回值类似的 float 对象。
               dt.timestamp() * 1000  则为转毫秒值  
        1.1.4. dt.weekday()  返回一个整数代表星期几，星期一为 0，星期天为 6。       
        1.1.5. dt.isoweekday()  返回一个整数代表星期几，星期一为 1，星期天为 7。      
                
    1.2. now = datetime.now() 获取当前时间  等价于 datetime.today()
    1.2. now = datetime.now() 获取当前时间
    1.3. datetime.strptime(date_str, format_str)  将字符串转换为时间对象。eg: str2time()

2. date 类表示日期（年、月、日），不包含时间信息。

    2.1. date.today()  返回当前的本地日期。这等价于 date.fromtimestamp(time.time())。
    2.2. date.fromtimestamp(timestamp)  返回对应于 POSIX 时间戳的当地时间，例如 time.time() 返回的就是时间戳。
    2.3. date.fromisoformat(date_string)  返回一个对应于只支持 YYYY-MM-DD 格式给出的 date_string 的 date 对象

3. time 类表示时间（时、分、秒、微秒），不包含日期信息。


4. timedelta 类表示两个日期(date)或时间(time)之间的时间间隔。
"""

# 1.3. 将字符串转换为时间对象
def str2time():
    # 输入的时间字符串
    date_str = "2024-01-19 at 09:57:37.183"
    # 定义时间字符串的格式
    format_str = "%Y-%m-%d at %H:%M:%S.%f"
    # 将字符串转换为时间对象
    time_obj = datetime.strptime(date_str, format_str)
    print(f"Converted time object: {time_obj}")