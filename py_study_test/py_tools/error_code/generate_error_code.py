# encoding: utf-8
import os
import sys
import time

from jinja2 import Environment, FileSystemLoader
from baidu_translate_util import translate_to_tw, translate_to_english

# 项目根路径
PROJECT_ROOT_PATH = f"{os.path.dirname(__file__)}/../../../"

# ErrorCode.java 所在目录
ERRORCODE_PATH = f"{PROJECT_ROOT_PATH}/hf-exception/src/main/java/com/cxx/hf/exception/ErrorCode.java"
# errorTips 配置生成目录
# ERROR_TIPS_DIR = f"{PROJECT_ROOT_PATH}/hf-servercore/src/main/resources"
ERROR_TIPS_DIR = "//10.198.141.130/sgp_dev/protocalGenSG/liuzhen/errorTips"


# keyStr 与 Command对象 映射
index_key_errorcode_list = [{}, {}, {}]
# 需要预警的错误码列表
need_alert_list = []
# 需要被翻译的列表
need_translate_list = []
# 错误码id集合
error_code_id_set = set()

"""
错误码对象
"""


class ErrorCode:
    def __init__(self, keyStr, cnText, enText, twText):
        self.keyStr = keyStr
        # 错误码key
        self.key = ''
        # 错误码序号
        self.id: int
        # 错误码中文
        self.cnText = cnText
        # 错误码英文
        self.enText = enText
        # 错误码繁体
        self.twText = twText

        self.__parse_keyStr()

    # 解析 keyStr
    def __parse_keyStr(self):
        split = self.keyStr.split(";")[0].split("=")
        if len(split) < 2:
            error_tips = f"ErrorCode 解析失败！错误码key value 格式不正确！错误码详情: {self.cnText}"
            raise RuntimeError(error_tips)

        self.key = split[0].replace(" ", "")
        self.id = split[1].replace(" ", "")


"""
生成错误码文件
"""


def general_error_code():
    try:
        # 1. 解析文件
        parse_file()
        # 2. 翻译文件
        translate()
        # 3. 生成文件
        do_general_error_code()
        # 4. 写入到properties文件中
        re_write_properties()
    except BaseException as e:
        print(e)
    finally:
        print("general error code success!")

"""
1. 解析 ErrorCode.java
"""


def parse_file():
    print("1. 开始解析ErrorCode.java ...")
    with open(f'{ERRORCODE_PATH}', 'r', encoding="utf-8") as file:

        index = 0
        while True:
            lineStr = file.readline()
            if lineStr == '':
                break

            if lineStr.find("// ↑↑↑↑↑↑↑") != -1:
                index = index + 1

            # 1.
            if lineStr.find("@Comment") != -1:
                keyStrLine = file.readline()
                if keyStrLine.find("public static final int ") == -1:
                    raise RuntimeError("ErrorCode 解析失败！错误码格式不正确！" + lineStr)

                keyStr = keyStrLine.split("public static final int ")[1].split("\n")[0]

                textArr = lineStr.split("(")[1].split(")")[0].split("\"")

                cnText = ""
                enText = ""
                twText = ""
                if len(textArr) >= 6:
                    cnText = textArr[1]
                    enText = textArr[3]
                    twText = textArr[5]
                elif len(textArr) >= 4:
                    cnText = textArr[1]

                    if lineStr.find("enText") != -1:
                        enText = textArr[3]
                    if lineStr.find("twText") != -1:
                        twText = textArr[3]
                elif len(textArr) >= 2:
                    cnText = textArr[1]

                if cnText == "" or len(cnText) <= 0:
                    raise RuntimeError("ErrorCode 解析失败！中文文本不能为空！" + lineStr)

                # 记录需要被翻译的list
                if enText == "" or len(enText) <= 0 or twText == "" or len(twText) <= 0:
                    need_translate_list.append(keyStr)

                error_code = ErrorCode(keyStr, cnText, enText, twText)
                # 错误码id重复校验
                if error_code.id in error_code_id_set:
                    raise RuntimeError("ErrorCode 解析失败！错误码id重复: " + error_code.id + " 文本: " + error_code.cnText)

                key_errorcode_list = index_key_errorcode_list[index]
                key_errorcode_list[keyStr] = error_code

                error_code_id_set.add(error_code.id)

            # 2. NEED_ALERT
            if lineStr.find("NEED_ALERT.add") != -1:
                s = lineStr.split("(")[1].split(")")[0]
                need_alert_list.append(s)


"""
2. 翻译
"""


def translate():
    print("2. 开始翻译...")
    for keyStr in need_translate_list:
        value = __get_error_code_ob(keyStr)
        if value == None:
            continue

        # 英文翻译
        if value.enText == '':
            value.enText = __format_english_word(translate_to_english(value.cnText))

        # 中文繁体翻译
        if value.twText == '':
            value.twText = translate_to_tw(value.cnText)


# 获取错误码对象
def __get_error_code_ob(keyStr: str):
    for error_code_dict in index_key_errorcode_list:
        if keyStr in error_code_dict:
            return error_code_dict[keyStr]
    return None


# 格式化英文翻译
def __format_english_word(word: str) -> str:
    if word.find("% ") != -1:
        word = word.replace("% ", "%")

    if word.find(":") != -1 & word.find(": ") == -1:
        word = word.replace(":", ": ")

    return word


"""
3. do 生成错误码文件
"""


def do_general_error_code():
    print("3. 开始生成错误码文件...")
    loader = FileSystemLoader(os.path.dirname(__file__), encoding='utf-8')
    env = Environment(loader=loader)
    template = env.get_template('errorcode.java.template')
    result = template.render(common_key_errorcode_list=index_key_errorcode_list[0], client_key_errorcode_list=index_key_errorcode_list[1],
                             other_key_errorcode_list=index_key_errorcode_list[2], need_alert_list=need_alert_list)

    # 写入文件中
    with open(f"{ERRORCODE_PATH}", 'wb') as file:
        file.write(result.encode('utf8'))


"""
4. 写入到properties文件中
"""


def re_write_properties():
    print("4. 开始写入到properties文件中...")

    # 配置文件
    properties_name_tuple = ("errorTips_zh_CN.properties", "errorTips_en_US.properties", "errorTips_zh_TW.properties")
    for name in properties_name_tuple:
        __do_re_write_properties(name)


# do 写入到properties文件中
def __do_re_write_properties(name):
    if not os.path.exists(ERROR_TIPS_DIR):
        os.makedirs(ERROR_TIPS_DIR)

    path = f"{ERROR_TIPS_DIR}/{name}"
    with open(path, "w", encoding="utf-8") as file:
        file.write(f"# --------------------Coder {os.getlogin()} Add new Properties--------------------\n")
        file.write(f"# 更新时间: {__get_format_time()}\n")

        for key_errorcode_dict in index_key_errorcode_list:
            for value in key_errorcode_dict.values():
                file.write(f"{value.id}={__get_text(path, value)}\n")


# 获取格式化时间
def __get_format_time():
    now = time.time()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    return formatted_time


# 获取文本内容
def __get_text(path: str, value):
    if path.find("errorTips_zh_CN") != -1:
        return value.cnText
    elif path.find("errorTips_en_US") != -1:
        return value.enText
    else:
        return value.twText


if __name__ == '__main__':
    args = sys.argv
    print(args)
    if len(args) >= 2 and len(args[1]) > 0:
        print(args)
        ERROR_TIPS_DIR = args[1] + "/errorTips"
        print("ERROR_TIPS_DIR: ", ERROR_TIPS_DIR)

    general_error_code()
