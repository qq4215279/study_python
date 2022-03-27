# encoding:utf-8

import sys
import os
import platform
import shutil
import stat
import argparse

IS_WIN = platform.system() == "Windows"

'''
打印日志
'''
def log(msg):
    print(msg)

'''
执行系统命令
没有命令输出，仅有状态码 0 表示成功、> 0 表示失败
'''
def execute(cmd):
    log("exec command " + cmd)
    if IS_WIN:
        if cmd.find("cd") != -1:
            cmd_array = cmd.split("&&")
            dir_path = cmd_array[0][3:].strip()
            log("exec chdir " + dir_path)
            os.chdir(dir_path)
            cmd = '&&'.join(cmd_array[1:]).strip()
    
    ret = os.system(cmd)
    log("exec command %s result %s"%(cmd, str(ret)))

    return ret

'''
执行系统命令
可以获取执行输出流
'''
def popen(cmd):
    log("exec command " + cmd)
    if IS_WIN:
        if cmd.find("cd") != -1:
            cmd_array = cmd.split("&&")
            dir_path = cmd_array[0][3:].strip()
            log("exec chdir " + dir_path)
            os.chdir(dir_path)
            cmd = '&&'.join(cmd_array[1:]).strip()
    
    ret = os.popen(cmd)

    return ret.readlines()

'''
删除只读文件
'''
def rm_read_only(fn, tmp, info):
    if os.path.isfile(tmp):
        os.chmod(tmp, stat.S_IWRITE)
        os.remove(tmp)
    elif os.path.isdir(tmp):
        os.chmod(tmp, stat.S_IWRITE)
        shutil.rmtree(tmp, onerror=rm_read_only)

'''
删除目录
'''
def rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path, onerror=rm_read_only)

'''
目录拷贝
'''
def copytree(fromPath, toPath, ignore=None):
    rmtree(toPath)

    shutil.copytree(fromPath, toPath, ignore=ignore)

'''
拷贝文件
'''
def copyFile(fromPath, toPath):
    if not os.path.exists(fromPath):
        return
    toBasePath = os.path.abspath(os.path.join(toPath, os.path.pardir))
    if not os.path.exists(toBasePath):
        os.makedirs(toBasePath)
    
    shutil.copy(fromPath, toPath)


'''
检出指定提交记录涉及的文件
'''
def pickCommitFiles(gitPath, commitId, outputPath=None):
    # git path 检查
    if not os.path.exists(gitPath):
        log("[ERROR]git path not exists, path:%s"%gitPath)
        return 1
    if not os.path.isdir(gitPath):
        log("[ERROR]git path must be a directory, path:%s"%gitPath)
        return 1

    # output path检查
    if outputPath == None:
        outputPath = gitPath


    # 1. 在指定目录执行pull操作
    cmd = "cd %s && git pull"%(gitPath)
    rtn = execute(cmd)
    if rtn != 0:
        log("[ERROR]git pull failed")
        return 1

    # 2. 过滤提交所涉及文件
    fileList = []
    commitArray = commitId.split(",")
    for _commitId in commitArray:
        result = popen('cd %s && git show %s --name-only'%(gitPath, _commitId))
        if result == None or len(result) < 7:
            log("no commit content")
            return 1
        for line in result[6:]:
            if line == None or line.strip() == '':
                continue
            if fileList.count(line.strip()) == 0:
                fileList.append(line.strip())

    # 3. 将这些文件提取到输出目录
    outputPath = os.path.join(outputPath, "output")
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    for f in fileList:
        log("copy file " + f)
        fromPath = os.path.join(gitPath, f)
        toPath = os.path.join(outputPath, f)

        copyFile(fromPath, toPath)

    log("output path " + outputPath)
    log("done")

'''
检出指定提交记录涉及的文件
'''
def pickDiffFiles(gitPath, commitId1, commitId2, outputPath=None):
    # git path 检查
    if not os.path.exists(gitPath):
        log("[ERROR]git path not exists, path:%s"%gitPath)
        return 1
    if not os.path.isdir(gitPath):
        log("[ERROR]git path must be a directory, path:%s"%gitPath)
        return 1

    # output path检查
    if outputPath == None:
        outputPath = gitPath


    # 1. 在指定目录执行pull操作
    cmd = "cd %s && git pull"%(gitPath)
    rtn = execute(cmd)
    if rtn != 0:
        log("[ERROR]git pull failed")
        return 1

    # 2. 过滤提交所涉及文件
    result = popen('cd %s && git diff --name-only %s %s'%(gitPath, commitId1, commitId2))
    if result == None or len(result) < 1:
        log("no diff content")
        return 1

    fileList = []
    for line in result:
        if line == None or line.strip() == '':
            continue
        fileList.append(line.strip())

    # 3. 将这些文件提取到输出目录
    outputPath = os.path.join(outputPath, "output")
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    for f in fileList:
        log("copy file " + f)
        fromPath = os.path.join(gitPath, f)
        toPath = os.path.join(outputPath, f)

        copyFile(fromPath, toPath)

    log("output path " + outputPath)
    log("done")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        log("[ERROR] args not enough")
        exit(1)

    print("-------------------->")

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help="pick mode [diff|commit]")
    parser.add_argument("-p", "--path", dest="path", help="git root path")
    parser.add_argument("-c", "--commit_id", dest="commitId", nargs="*", help="git commit id")
    parser.add_argument("-o", "--output", dest="output", help="output path")

    options = parser.parse_args(sys.argv[1:])
    if options.mode == "diff":
        pickDiffFiles(options.path, options.commitId[0], options.commitId[1], options.output)
    else:
        pickCommitFiles(options.path, options.commitId[0], options.output)

