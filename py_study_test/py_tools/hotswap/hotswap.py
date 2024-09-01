# encoding:utf-8

import os
import sys
import shutil

# 代理jar包路径
AGENT_JAR_PATH = "game-agent.jar"
# 项目根路径
BASE_PROJECT_PAH = "F:\Code\WorkSpace\yjxxl_server\\app\\trunk\hf-parent"
# 默认执行附载进程
DEFAULT_PROCESS_NAMES = "com.cxx.hf.servergame.GameStart;com.cxx.hf.serverhall.HallStart;com.cxx.hf.serverplatform.PlatformStart;com.cxx.hf.serverplayer.PlayerStart"

# 默认最新字节码文件所在目录
DEFAULT_CLASSES_PATH = f"{os.getcwd()}/target"

"""
获取参数信息
"""
def get_args():
    classNames = ''
    classesPath = ''
    attachProcessNames = ''
    for arg in sys.argv:
        if arg.find("=") == -1:
            continue

        arr = arg.split("=")
        if arr[0] == 'classNames':
            classNames = arr[1]
        if arr[0] == 'classesPath':
            classesPath = arr[1]
        if arr[0] == 'attachProcessNames':
            attachProcessNames = arr[1]

    if classesPath == '':
        copy_classes(classNames)
        classesPath = DEFAULT_CLASSES_PATH
    if attachProcessNames == '':
        attachProcessNames = DEFAULT_PROCESS_NAMES

    return classNames, classesPath, attachProcessNames


"""
拷贝最新字节码文件
"""
def copy_classes(classNames):
    if os.path.exists(DEFAULT_CLASSES_PATH):
        # os.removedirs(DEFAULT_CLASSES_PATH)
        shutil.rmtree(DEFAULT_CLASSES_PATH)
    os.mkdir(DEFAULT_CLASSES_PATH)

    split = classNames.split(";")
    for className in split:
        classes_path = get_classes_path(className)

        arr = className.split(".")
        shortClassName = arr[len(arr) - 1]
        # 拷贝文件
        shutil.copyfile(classes_path, f"{DEFAULT_CLASSES_PATH}/{shortClassName}.class")

"""
获取 classesPath 绝对路径
"""
def get_classes_path(className: str):
    split = className.split(".")
    module_name = split[2] + "-" + split[3]
    # print("module_name: " + module_name)

    classes_path = BASE_PROJECT_PAH + f"\\{module_name}\\target\\classes\\" + className.replace(".", "\\") + ".class"
    # print("classes_path: " + classes_path)
    return classes_path

"""
执行动更
"""
def load_agent(classNames: str, classesPath: str, attachProcessNames: str):
    try:
        command = f"java -jar {AGENT_JAR_PATH} classNames={classNames} classesPath={classesPath} attachProcessNames={attachProcessNames}"
        os.system(command)
    except BaseException as e:
        print("py load Agent fail...")
        print(e)

if __name__ == '__main__':
    args = get_args()
    classNames = args[0]
    classesPath = args[1]
    attachProcessNames = args[2]

    print("classNames: " + classNames)
    print("classesPath: " + classesPath)
    print("attachProcessNames: " + attachProcessNames)

    # 执行动更
    load_agent(classNames, classesPath, attachProcessNames)