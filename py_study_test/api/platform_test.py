# encoding: utf-8

import platform

# 获取操作系统相关信息
print("Operating System:", platform.system())
print("Operating System Version:", platform.release())
print("Platform:", platform.platform())
print("System Information:", platform.uname())

# 获取Python解释器相关信息
print("Python Version:", platform.python_version())
print("Python Implementation:", platform.python_implementation())
print("Python Build Information:", platform.python_build())
print("Python Compiler:", platform.python_compiler())

# 获取硬件相关信息
print("Machine:", platform.machine())
print("Processor:", platform.processor())
print("Node:", platform.node())
print("Architecture:", platform.architecture())

# 获取网络相关信息
print("Network Name:", platform.node())


