# encoding: utf-8

import platform

# 获取操作系统相关信息
print("Operating System:", platform.system())  # Operating System: Windows
print("Operating System Version:", platform.release())  # Operating System Version: 10
print("Platform:", platform.platform())  # Platform: Windows-10-10.0.19041-SP0
# System Information: uname_result(system='Windows', node='mumu996', release='10', version='10.0.19041', machine='AMD64', processor='Intel64 Family 6 Model 151 Stepping 2, GenuineIntel')
print("System Information:", platform.uname())

# 获取Python解释器相关信息
print("Python Version:", platform.python_version())  # Python Version: 3.8.5
print("Python Implementation:", platform.python_implementation())  # Python Implementation: CPython
print("Python Build Information:", platform.python_build())  # Python Build Information: ('tags/v3.8.5:580fbb0', 'Jul 20 2020 15:43:08')
print("Python Compiler:", platform.python_compiler())  # Python Compiler: MSC v.1926 32 bit (Intel)

# 获取硬件相关信息
print("Machine:", platform.machine())  # Machine: AMD64
print("Processor:", platform.processor())  # Processor: Intel64 Family 6 Model 151 Stepping 2, GenuineIntel
print("Node:", platform.node())  # Node: mumu996
print("Architecture:", platform.architecture())  # Architecture: ('32bit', 'WindowsPE')

# 获取网络相关信息
print("Network Name:", platform.node())  # Network Name: mumu996


