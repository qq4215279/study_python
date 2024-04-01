# encoding: utf-8

import subprocess

"""
subprocess 
是 Python 标准库中用于创建和管理新进程的模块。它提供了一个强大的接口，可以与操作系统交互，执行外部命令，以及与这些命令的输入、输出和错误流进行交互。

常用api: 
1. subprocess.run()	 执行指定的命令，等待命令执行完成后返回一个包含执行结果的 CompletedProcess 类的实例。
    eg: subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, timeout=None, check=False, universal_newlines=False)
2. subprocess.call()	执行指定的命令，返回命令执行状态，其功能类似于os.system(cmd)。
    eg: subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False, timeout=None)
3. subprocess.check_call()	执行指定的命令，如果执行成功则返回状态码，否则抛出异常。其功能等价于subprocess.run(…, check=True)。
    eg: subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False, timeout=None)
4. subprocess.check_output()	执行指定的命令，如果执行状态码为0则返回命令执行结果，否则抛出异常。
    eg: res = subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False, timeout=None)
5. subprocess.getoutput(cmd)	接收字符串格式的命令，执行命令并返回执行结果，其功能类似于os.popen(cmd).read()和commands.getoutput(cmd)。
    eg: res = subprocess.getoutput(cmd)
6. subprocess.getstatusoutput(cmd)	执行cmd命令，返回一个元组(命令执行状态, 命令执行结果输出)，其功能类似于commands.getstatusoutput()。
    eg: retcode, output = subprocess.getstatusoutput('ls -l')

参数说明: 
1. args: 要执行的shell命令，默认应该是一个字符串序列，如[‘df’, ‘-Th’]或(‘df’, ‘-Th’)，也可以是一个字符串，如’df -Th’，但是此时需要把shell参数的值置为True。
2. shell: 如果shell为True，那么指定的命令将通过shell执行。如果我们需要访问某些shell的特性，如管道、文件名通配符、环境变量扩展功能，这将是非常有用的。当然，python本身也提供了许多类似shell的特性的实现，如glob、fnmatch、os.walk()、os.path.expandvars()、os.expanduser()和shutil等。
3. check: 如果check参数的值是True，且执行命令的进程以非0状态码退出，则会抛出一个CalledProcessError的异常，且该异常对象会包含 参数、退出状态码、以及stdout和stderr(如果它们有被捕获的话)。
4. stdout, stderr：input: 该参数是传递给Popen.communicate()，通常该参数的值必须是一个字节序列，如果universal_newlines=True，则其值应该是一个字符串。
    run()函数默认不会捕获命令执行结果的正常输出和错误输出，如果我们向获取这些内容需要传递subprocess.PIPE，然后可以通过返回的CompletedProcess类实例的stdout和stderr属性或捕获相应的内容；
    call()和check_call()函数返回的是命令执行的状态码，而不是CompletedProcess类实例，所以对于它们而言，stdout和stderr不适合赋值为subprocess.PIPE；
    check_output()函数默认就会返回命令执行结果，所以不用设置stdout的值，如果我们希望在结果中捕获错误信息，可以执行stderr=subprocess.STDOUT。
5. universal_newlines： 该参数影响的是输入与输出的数据格式，比如它的值默认为False，此时stdout和stderr的输出是字节序列；当该参数的值设置为True时，stdout和stderr的输出是字符串。


subprocess.CompletedProcess 调用 subprocess.run()函数，返回值是一个 subprocess.CompletedPorcess 类的实例，因此，subprocess.completedPorcess 表示的是一个已结束进程的状态信息
属性如下: 
    args: 用于加载该进程的参数，这可能是一个列表或一个字符串
    returncode: 进程的退出状态码。通常情况下，退出状态码为0则表示进程成功运行了；一个负值-N表示这个子进程被信号N终止了
    stdout: 从子进程捕获的stdout。这通常是一个字节序列，如果run()函数被调用时指定universal_newlines=True，则该属性值是一个字符串。
        如果run()函数被调用时指定stderr=subprocess.STDOUT，那么stdout和stderr将会被整合到这一个属性中，且stderr将会为None
    stderr: 从子进程捕获的stderr。它的值与stdout一样，是一个字节序列或一个字符串。如果stderr灭有被捕获的话，它的值就为None
    check_returncode(): 如果returncode是一个非0值，则该方法会抛出一个CalledProcessError异常。


subprocess.Popen
上面介绍的这些函数都是基于subprocess.Popen类实现的，通过使用这些被封装后的高级函数可以很方面的完成一些常见的需求。

1.构造函数
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False,
    startup_info=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=())

参数说明: 
    args: 要执行的shell命令，可以是字符串，也可以是命令各个参数组成的序列。当该参数的值是一个字符串时，该命令的解释过程是与平台相关的，因此通常建议将args参数作为一个序列传递。
    bufsize: 指定缓存策略，0表示不缓冲，1表示行缓冲，其他大于1的数字表示缓冲区大小，负数 表示使用系统默认缓冲策略。
    stdin, stdout, stderr: 分别表示程序标准输入、输出、错误句柄。
    preexec_fn: 用于指定一个将在子进程运行之前被调用的可执行对象，只在Unix平台下有效。
    close_fds: 如果该参数的值为True，则除了0,1和2之外的所有文件描述符都将会在子进程执行之前被关闭。
    shell: 该参数用于标识是否使用shell作为要执行的程序，如果shell值为True，则建议将args参数作为一个字符串传递而不要作为一个序列传递。
    cwd: 如果该参数值不是None，则该函数将会在执行这个子进程之前改变当前工作目录。
    env: 用于指定子进程的环境变量，如果env=None，那么子进程的环境变量将从父进程中继承。如果env!=None，它的值必须是一个映射对象。
    universal_newlines: 如果该参数值为True，则该文件对象的stdin，stdout和stderr将会作为文本流被打开，否则他们将会被作为二进制流被打开。
    startupinfo和creationflags: 这两个参数只在Windows下有效，它们将被传递给底层的CreateProcess()函数，用于设置子进程的一些属性，如主窗口的外观，进程优先级等。

subprocess.Popen 类的实例可调用的方法  eg: popen = subprocess.Popen()
1. popen.poll()	用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码。
2. popen.wait(timeout=None)	等待子进程结束，并返回状态码；如果在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。
3. popen.communicate(input=None, timeout=None)	该方法可用来与进程进行交互，比如发送数据到stdin，从stdout和stderr读取数据，直到到达文件末尾。
4. popen.send_signal(signal)	发送指定的信号给这个子进程。
5. popen.terminate()	停止该子进程。
6. popen.kill()	杀死该子进程。
"""

# 指定工作目录
working_directory = f"E:/Doc/buyu1cehua/tools/xlsx2jsonAndXml"
process = subprocess.Popen(["export-jsonAndxml4Py.bat"], stdin=subprocess.PIPE, cwd=working_directory,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# 向标准输入发送一个回车键，模拟按任意键继续
output, _ = process.communicate(input=b'\n')
print(output.decode("gbk"))

# run
subprocess.run(["ls", "-l"])  # doesn't capture output
subprocess.run("exit 1", shell=True, check=True)

# call
subprocess.call(['ls', '-l'])
subprocess.call('ls -l', shell=True)
subprocess.call(['ls', '-l'], stdout=subprocess.DEVNULL)

# check_call
subprocess.check_call(['ls', '-l'])
subprocess.check_call('ls -l', shell=True)

# check_output
ret = subprocess.check_output(['ls', '-l'])
print(ret)

# getoutput
ret = subprocess.getoutput('ls -l')
print(ret)

# getstatusoutput
retcode, output = subprocess.getstatusoutput('ls -l')
print(retcode)

# Popen
p = subprocess.Popen('df -Th', stdout=subprocess.PIPE, shell=True)
print(p.stdout.read())

obj = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
obj.stdin.write('print(1) \n')
obj.stdin.write('print(2) \n')
obj.stdin.write('print(3) \n')
out, err = obj.communicate()
print(out)

obj = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = obj.communicate(input='print(1) \n')
