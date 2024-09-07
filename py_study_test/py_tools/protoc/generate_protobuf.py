# encoding: utf-8

import os
from jinja2 import Environment, FileSystemLoader

# 项目根路径
# PROJECT_ABPATH = f"{os.path.dirname(__file__)}/../../../"
# 协议所在路径
# PROTO_PATH = f"{PROJECT_ABPATH}/AutoGen/src/main/resources/proto"
# 生成实体类所在目录
# POJO_PATH = f"{PROJECT_ABPATH}/AutoGen/src/main/java"

# 项目根路径
PROJECT_ABPATH = f"D:/Code/IdeaWorkSpace/coding_plan/tech_enhance"
# 协议所在路径
PROTO_PATH = f"{PROJECT_ABPATH}/src/main/resources/proto"
# 生成实体类所在目录
POJO_PATH = f"{PROJECT_ABPATH}/src/main/java"

# proto协议文件路径 与 Proto对象映射
PROTO_FILE_DICT = dict()
# 协议名 与 对应包路径
MESSAGE_NAME_PACKAGE_PATH_DICT = dict()

# message 协议类型
MESSAGE_TYPE = "message"
# enum 协议类型
ENUM_TYPE = "enum"

# 协议映射
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

"""
协议文件
"""
class Proto:
    def __init__(self):
        # 协议绝对路径
        self.abPath = ""
        # 包目录
        self.java_package = ""
        # 导入的protoc文件
        self.imports = list()
        # Message 列表
        self.message_dict = dict()
        # 文件所有行信息
        self.lines = list()


"""
协议
"""
class Message:
    # 协议类型: 1: Message; 2: Enum
    type: str
    # 注释
    notes: str
    # 协议名
    name: str
    # 协议字段
    fields = list()

    def __init__(self):
        self.type = ""
        self.notes = ""
        self.name = ""
        self.fields = list()


"""
枚举协议字段
"""
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


"""
Message消息协议字段
"""
class MField(EField):
    # 字段规则: repeated TODO 当前仅支持 repeated
    field_rule: str
    # 字段类型
    field_type: str
    # Java字段类型
    java_field_type: str

    def __init__(self):
        self.field_rule = ""
        self.field_type = ""
        self.java_field_type = ""


"""
proto -> java
"""
def general_proto_buff(proto_files=list()):
    # 1. 获取所有proto协议文件
    print("1. start 获取所有proto协议文件...")
    proto_file_paths = __get_all_proto_file_paths(proto_files)
    print("1. end 获取所有proto协议文件...\n")

    # 2. 解析proto文件
    print("2. start 解析proto文件...")
    _parse_protos(proto_file_paths)
    print("2. end 解析proto文件...\n")

    # 3. 渲染生成客户端proto文件
    print("3. start 解析proto文件...")
    _render_protos_template()
    print("3. end 解析proto文件...\n")

    # 4. 渲染生成Java实体
    print("4. start 渲染生成Java实体...")
    _render_java_template()
    print("4. end 渲染生成Java实体...")


"""
1. 获取所有proto协议文件
"""
def __get_all_proto_file_paths(proto_files=list()) -> list:
    all_files = list()
    for root, dirs, files in os.walk(PROTO_PATH):
        for file in files:
            if len(proto_files) <= 0 or file in proto_files:
                all_files.append(os.path.join(root, file))

    return all_files


"""
2. 解析所有proto文件
"""
def _parse_protos(proto_file_paths):
    for proto_file_path in proto_file_paths:
        __parse_proto(proto_file_path)

# do 解析所有proto文件
def __parse_proto(proto_file_path):
    proto = Proto()
    with open(f"{proto_file_path}", 'r', encoding="utf-8") as source_file:
        PROTO_FILE_DICT[proto_file_path] = proto
        proto.abPath = proto_file_path

        start_parse_message = False
        # 协议名
        message_name = ""
        # 协议类型: 1: message; 2: enum
        message_type: str
        # 协议注释
        message_notes = ""
        # 字段注释
        field_notes = ""
        # order
        field_order = 1

        for line in source_file.readlines():
            # 开始解析协议信息
            if start_parse_message:
                # 结束协议
                if line.find("}") != -1:
                    start_parse_message = False
                    message_notes = ""
                    field_notes = ""
                    field_order = 1

                    # TODO 目前定义协议，需要需要加等号=
                elif line.find("=") != -1:
                    message = proto.message_dict[message_name]
                    # 初始化
                    if len(message.fields) <= field_order - 1:
                        filed = None
                        # Message
                        if message_type == MESSAGE_TYPE:
                            filed = MField()
                        # Enum
                        elif message_type == ENUM_TYPE:
                            filed = EField()
                        filed.notes = field_notes.replace("\n", "")
                        message.fields.append(filed)

                    filed = message.fields[field_order - 1]

                    arr = __parse_eq_line(line)
                    length = len(arr)
                    # repeated int64 playerIds
                    if length >= 3:
                        filed.field_rule = arr[0]
                        filed.field_type = arr[1]
                        filed.java_field_type = __convert_2_java_fields(filed.field_type)
                        filed.field_name = arr[2]

                        # int64 playerIds
                    elif length >= 2:
                        filed.field_type = arr[0]
                        filed.field_name = arr[1]
                        filed.java_field_type = __convert_2_java_fields(filed.field_type)

                        # 枚举协议 eg: READY = 0;
                    elif length >= 1:
                        filed.field_name = arr[0]

                    filed.notes = field_notes.replace("\n", "")
                    filed.field_order = field_order

                    # reset
                    field_notes = ""
                    field_order += 1

                # TODO 注释处理：目前仅支持注释与协议定义不在同一行  暂时默认其他行都是注释
                else:
                    field_notes += line

            # 解析 Message 协议
            elif line.find(MESSAGE_TYPE) != -1 and line.find("{") != -1:
                start_parse_message = True
                message_type = MESSAGE_TYPE

                message_name = __parse_message(message_type, line, message_notes, proto)
                message_notes = ""

            # 解析 enum 协议
            elif line.find(ENUM_TYPE) != -1 and line.find("{") != -1:
                start_parse_message = True
                message_type = ENUM_TYPE

                message_name = __parse_message(message_type, line, message_notes, proto)
                message_notes = ""

                # 解析 java_package 目录 TODO java_package 定义必须在所有协议最前面！
            elif line.find("java_package") != -1:
                proto.lines.append(line)

                java_package = line.split("\"")[1].strip()
                # print("   java_package: ", java_package)
                proto.java_package = java_package

                # 解析导入的包 import "baloot/baloot.proto";
            elif line.find("import ") != -1:
                proto.lines.append(line)
                im = line.split("\"")[1].strip()
                print("import: ", im)
                proto.imports.append(im)

            # 记录行信息
            else:
                proto.lines.append(line)
                if line.find("syntax") == -1:
                    message_notes += line


# 协议行信息
def __parse_eq_line(line: str):
    arr = line.split("=")[0].strip().split(" ")
    # 去除掉数组中的空字符串
    return [string for string in arr if string.strip()]

# 解析协议信息
def __parse_message(proto_type: str, line: str, proto_notes: str, proto: Proto):
    # 截取协议名
    message_name = line.split(proto_type)[1].split("{")[0].strip()

    proto.lines.append(f"###{message_name}")

    new_message = Message()
    new_message.name = message_name
    new_message.type = proto_type
    new_message.notes = proto_notes.replace("\n", "").replace("//", "").replace("/*", "").replace("/**", "").replace(
        "*/", "")

    proto.message_dict[message_name] = new_message
    MESSAGE_NAME_PACKAGE_PATH_DICT[message_name] = proto.java_package

    return message_name

# 字段转Java类型
def __convert_2_java_fields(field_type: str):
    if field_type in FieldType_DICT:
        return FieldType_DICT[field_type]
    else:
        return field_type

"""
3. 渲染生成客户端proto文件
"""
def _render_protos_template():
    for proto_path, proto in PROTO_FILE_DICT.items():
        __render_proto_template(proto)

# do 渲染proto模板
def __render_proto_template(proto: Proto):
    loader = FileSystemLoader(os.path.dirname(__file__), encoding='utf-8')
    env = Environment(loader=loader)
    template = env.get_template('proto.template')
    result = template.render(proto=proto)

    # 写入文件中
    with open(f"{proto.abPath}", 'wb') as file:
        file.write(result.encode('utf8'))

    print("  render proto success! proto_path: ", proto.abPath)

"""
4. 渲染生成所有Java实体
"""
def _render_java_template():
    for proto_path, proto in PROTO_FILE_DICT.items():
        print("  start render proto: ", proto.abPath)
        for message_name, message in proto.message_dict.items():
            __do_render_java_template(proto.java_package, message)
        print("\n")

# do 渲染生成Java实体
def __do_render_java_template(java_package: str, message: Message):
    imports = __find_all_import_packages(java_package, message)
    clazz_type_name = __get_clazz_type_name(message.type)

    loader = FileSystemLoader(os.path.dirname(__file__), encoding='utf-8')
    env = Environment(loader=loader)
    template = env.get_template('proto.to.java.template')
    result = template.render(package=java_package, imports=imports, clazz_type_name=clazz_type_name, message=message)

    # 目标文件目录
    dest_java_dir = f"{POJO_PATH}/{java_package.replace('.', '/')}"
    if not os.path.exists(dest_java_dir):
        os.makedirs(dest_java_dir)

    dest_java_path = f"{dest_java_dir}/{message.name}.java"
    # 写入文件中
    with open(dest_java_path, 'wb') as file:
        file.write(result.encode('utf8'))

    print("    render java success! dest_java_path: ", dest_java_path)

# 找需要 import 包
def __find_all_import_packages(java_package: str, message: Message) -> list:
    packages = list()
    # 枚举
    if message.type == ENUM_TYPE:
        return packages

    # class
    for field in message.fields:
        # 在相同包下的协议，无需导包
        if field.field_type not in FieldType_DICT and java_package != MESSAGE_NAME_PACKAGE_PATH_DICT[field.field_type]:
            packages.append(MESSAGE_NAME_PACKAGE_PATH_DICT[field.field_type] + "." + field.field_type)

    return packages

# 获取类文件类型
def __get_clazz_type_name(message_type) -> str:
    if message_type == MESSAGE_TYPE:
        return "class"
    else:
        return "enum"


if __name__ == '__main__':
    # 指定协议名，则只处理指定协议文件，不指定默认选择所有proto文件
    # proto_files = ["baloot.proto"]
    proto_files = []
    general_proto_buff(proto_files)