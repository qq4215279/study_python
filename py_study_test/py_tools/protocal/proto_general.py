# encoding: utf-8

import os
import os.path as path

# 项目所在绝对路径
PROJECT_ABPATH = "../../"
# 协议生成目录。默认当前目录
OUT_PATH = "../client/"

"""
生成客户端proto文件
"""
def general_client_proto():
  # 协议所在路径
  proto_path = f"{PROJECT_ABPATH}/AutoGen/src/main/resources/proto"

  # 1. 获取所有proto协议文件
  proto_file_paths = __get_all_proto_file_paths(proto_path)
  # print(proto_file_paths)

  # 2. 生成客户端proto文件
  __do_general_client_proto(proto_file_paths)


"""
获取所有proto协议文件
"""
def __get_all_proto_file_paths(dirPath: str) -> list:
  files = []

  for fileName in os.listdir(dirPath):
    ab_path = f"{dirPath}/{fileName}"
    if path.isdir(ab_path):
      files.extend(__get_all_proto_file_paths(f"{dirPath}/{fileName}"))
    else:
      files.append(ab_path)

  return files


"""
do 生成客户端proto文件
"""
def __do_general_client_proto(proto_file_paths):
  with open(f'{OUT_PATH}/client.proto', 'w', encoding="utf-8") as dst_file:
    first = True

    for proto_file_path in proto_file_paths:
      with open(f"{proto_file_path}", 'r',
                encoding="utf-8") as source_file:
        for readline in source_file.readlines():
          if readline.find("java_package") != -1:
            continue
          if readline.find("import ") != -1:
            continue

          if readline.find("syntax") != -1 and not first:
            continue

          first = False
          dst_file.writelines(readline)


if __name__ == '__main__':
  general_client_proto()
