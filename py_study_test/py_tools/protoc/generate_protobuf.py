# encoding: utf-8

import os
import sys
import time

from jinja2 import Environment, FileSystemLoader


# 项目根路径
PROJECT_ABPATH = f"{os.path.dirname(__file__)}/../../../"

FieldType_DICT = {
    "double": "Double",
    "float": "Float",
    "int64": "Long",
    "uint64": "Long",
    "int32": "Integer",
    "fixed64": "Long",
    "fixed32": "Integer",
    "bool": "Boolean",
    "string": "String",
    "bytes": "bytes",
    "uint32": "Integer",
    "sfixed32": "Integer",
    "sfixed64": "Long",
    "sint32": "Integer",
    "sint64": "Long",
    "object": "Object",
    "enum": "Enum",
    "map": "Map",
}

# 协议路径 与 ProtoFile对象映射
PROTO_FILE_DICT = dict()
# 协议名 与 对应包路径
PROTO_NAME_PACKGE_PATH_DICT = dict()

"""
协议文件
"""
class ProtoFile:
    def __init__(self):
        # 协议绝对路径
        self.abPath = ""
        # 包目录
        self.java_package = ""
        # 导入的protoc文件
        self.imports = list()
        # Message 列表
        self.proto_dict = dict()
        # 文件所有行信息
        self.lines = list()
        # 协议(Message & Enum)注释: 协议名 : 注释
        self.proto_notes = dict()

# 协议
class Proto:
    # 协议名
    name: str
    # 协议类型: 1: Message; 2: Enum
    type: int
    # 注释
    notes: str
    # 协议字段
    fields = list()

    def __init__(self):
        self.name = ""
        self.type = 0
        self.notes = ""
        self.fields = list()


# 枚举协议字段
class EField:
    # 注释
    notes: str
    # 字段名
    field_name: str
    # 字段序列
    field_order: int

    def __init__(self):
        self.notes = ""
        self.field_name = ""
        self.field_order = 1

# Message消息协议字段
class MField(EField):
    # 字段规则: repeated TODO 当前仅支持 repeated
    field_rule: str
    # 字段类型
    field_type: str

    def __init__(self):
        self.field_rule = ""
        self.field_type = ""


"""


"""
def general_protobuff():
    #
    # 协议所在路径
    proto_path = f"{PROJECT_ABPATH}/AutoGen/src/main/resources/proto"

    # 1. 获取所有proto协议文件
    proto_file_paths = __get_all_proto_file_paths(proto_path)

    # 2. 生成客户端proto文件
    __do_general_client_proto(proto_file_paths)


"""
获取所有proto协议文件
"""
def __get_all_proto_file_paths(dirPath: str) -> list:
  files = []

  for fileName in os.listdir(dirPath):
    ab_path = f"{dirPath}/{fileName}"
    if os.path.isdir(ab_path):
      files.extend(__get_all_proto_file_paths(f"{dirPath}/{fileName}"))
    else:
      files.append(ab_path)

  return files


"""
do 生成客户端proto文件
"""
def __do_general_client_proto(proto_file_paths):
    for proto_file_path in proto_file_paths:
        method_name(proto_file_path)


def method_name(proto_file_path):
    protoFile = ProtoFile()
    with open(f"{proto_file_path}", 'r', encoding="utf-8") as source_file:
        PROTO_FILE_DICT[proto_file_path] = protoFile
        protoFile.abPath = proto_file_path

        # 协议名
        proto_name = ""
        startProto = False
        # 协议类型: 1: Message; 2: Enum
        proto_type: int
        # 协议注释
        proto_notes = ""

        # 字段注释
        field_notes = ""
        # order
        field_order = 1

        for readline in source_file.readlines():
            # 开始记录协议信息
            if startProto:
                # 结束协议
                if readline.find("}") != -1:
                    # 还有注释
                    if field_notes != "":
                        # TODO
                        # Message
                        if proto_type == 1:
                            filed = MField()
                            filed.notes = field_notes.replace("\n", "")
                            proto.fields.append(filed)
                        # Enum
                        elif proto_type == 2:
                            filed = EField()
                            filed.notes = field_notes.replace("\n", "")
                            proto.fields.append(filed)
                        field_notes = ""

                    startProto = False
                    proto_notes = ""
                    field_order = 1

                    # TODO 目前定义协议，需要需要加等号=
                elif readline.find("=") != -1:
                    proto = protoFile.proto_dict[proto_name]
                    # 初始化
                    if len(proto.fields) <= field_order - 1:
                        # Message
                        if proto_type == 1:
                            filed = MField()
                            filed.notes = field_notes.replace("\n", "")
                            proto.fields.append(filed)
                        # Enum
                        elif proto_type == 2:
                            filed = EField()
                            filed.notes = field_notes.replace("\n", "")
                            proto.fields.append(filed)


                    filed = proto.fields[field_order - 1]
                    arr = readline.split("=")[0].strip().split(" ")
                    length = len(arr)
                    # repeated int64 playerIds
                    if length >= 3:
                        filed.field_rule = arr[0]
                        filed.field_type = arr[1]
                        filed.field_name = arr[2]
                    elif length >= 2:
                        filed.field_type = arr[0]
                        filed.field_name = arr[1]

                        # 枚举协议 eg: READY = 0;
                    elif length >= 1:
                        filed.field_name = arr[0]

                    filed.notes = field_notes.replace("\n", "")
                    filed.field_order = field_order

                    # reset
                    field_notes = ""
                    field_order += 1

                # TODO 注释处理：目前仅支持注释与协议定义不在同一行
                # elif readline.find("//") != -1 or readline.find("/*") != -1:
                # TODO 暂时默认其他行都是注释
                else:
                    field_notes += readline

            # Message 协议
            elif readline.find("message ") != -1 and readline.find("{") != -1:
                proto_name = readline.split("message")[1].split("{")[0].strip()

                protoFile.lines.append(f"###{proto_name}")

                startProto = True
                proto_type = 1

                new_proto = Proto()
                new_proto.name = proto_name
                new_proto.type = proto_type
                new_proto.notes = proto_notes.replace("\n", "")
                proto_notes = ""

                protoFile.proto_dict[proto_name] = new_proto
                PROTO_NAME_PACKGE_PATH_DICT[proto_file_path] = protoFile.java_package

            elif readline.find("enum ") != -1 and readline.find("{") != -1:
                proto_name = readline.split("enum")[1].split("{")[0].strip()
                protoFile.lines.append(f"###{proto_name}")

                startProto = True
                proto_type = 2

                new_proto = Proto()
                new_proto.name = proto_name
                new_proto.type = proto_type
                new_proto.notes = proto_notes.replace("\n", "")
                proto_notes = ""

                protoFile.proto_dict[proto_name] = new_proto
                PROTO_NAME_PACKGE_PATH_DICT[proto_file_path] = protoFile.java_package

                # option java_package = "com.game.proto.basegame";
                # TODO java_package 定义必须在协议最前面！
            elif readline.find("java_package") != -1:
                protoFile.lines.append(readline)

                java_package = readline.split("\"")[1].strip()
                print("java_package: ", java_package)
                protoFile.java_package = java_package

                # import "login/login.proto";
                # import "baloot/baloot.proto";
            elif readline.find("import ") != -1:
                protoFile.lines.append(readline)
                im = readline.split("\"")[1].strip()
                print("import: ", im)
                protoFile.imports.append(im)

            # 有注释
            # elif readline.find("//") != -1 or readline.find("/*") != -1:
            else:
                protoFile.lines.append(readline)
                proto_notes += readline

    print("end....")
    return protoFile


"""

"""
def render_proto_template(projectFile: ProtoFile):
    print("3. 开始生成错误码文件...")
    loader = FileSystemLoader(os.path.dirname(__file__), encoding='utf-8')
    env = Environment(loader=loader)
    template = env.get_template('proto.template')
    result = template.render(projectFile=projectFile)

    # 写入文件中
    with open(f"D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\py_tools\\protoc\\game.proto", 'wb') as file:
        file.write(result.encode('utf8'))


def render_java_template():
    pass

if __name__ == '__main__':
    path = "D:\\Code\\IdeaWorkSpace\\coding_plan\\tech_enhance\\src\main\\resources\\proto\\basegame\\game.proto"
    projectFile = method_name(path)
    render_proto_template(projectFile)