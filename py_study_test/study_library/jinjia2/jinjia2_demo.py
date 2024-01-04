# encoding:utf-8

from jinja2 import Template, Environment, FileSystemLoader

"""
jinjia2包: 作为一个模板系统，它还提供了特殊的语法，我们按照它支持的语法进行编写之后，就能使用jinja2模块进行渲染。

0. Enviroment: 用于存储配置和全局对象，然后从文件系统或其他位置中加载模板。即用它加载模板。
    Environment支持两种加载方式：
        PackageLoader: 包加载器。PackageLoader()的两个参数为: python包的名称，以及模板目录名称。
            eg: env = Environment(loader=PackageLoader('python_project','templates'))    # 创建一个包加载器对象
        FileSystemLoader: 文件系统加载器，不需要模板文件存在某个Python包下，可以直接访问系统中的文件。
        eg: 
    使用env: 获取一个模板文件: env.get_template(): 获取模板目录下的某个具体文件。eg: template = env.get_template('bast.html')

1. 创建模板:
    1.1. 创建字符串模板: eg: template = Template(template_string)
    1.2. 创建带有数据的文件模板: 使用文件系统加载模板。
        步骤如下: 
            # 1. 创建一个加载器对象，指定模板文件所在的目录
            loader = FileSystemLoader('templates')
            # 2. 创建一个环境对象，指定加载器
            env = Environment(loader=loader)
            # 3. 通过环境对象获取模板
            template = env.get_template('hello.html')

2. 渲染模板: template.render(): 接受变量，对模板进行渲染，返回被渲染的模板信息。
    str = template.render()

3. 模板语法:
    3.1. 变量取值: {{ }}
        它是一种特殊的占位符。当利用jinja2进行渲染的时候，它会把这些特殊的占位符进行填充/替换，jinja2支持python中所有的Python数据类型比如列表、字段、对象等。
    3.2. 控制结构 {% %}
        3.2.1. if条件: if语句类似与Python的if语句，它也具有单分支，多分支等多种结构，不同的是，条件语句不需要使用冒号结尾，而结束控制语句，需要使用endif关键字。
            {% if daxin.safe %}
                daxin is safe.
            {% elif daxin.dead %}
                daxin is dead
            {% else %}
                daxin is okay
            {% endif %}
         3.2.2. for循环: for循环用于迭代Python的数据类型，包括列表，元组和字典。在jinja2中不存在while循环。
            当然也可以加入else语句，在循环正确执行完毕后，执行
            在for循环中，jinja2还提供了一些特殊的变量，用以来获取当前的遍历状态：
                loop.index	当前迭代的索引（从1开始）
                loop.index0	当前迭代的索引（从0开始）
                loop.first	是否是第一次迭代，返回bool
                loop.last	是否是最后一次迭代，返回bool
                loop.length	序列中的项目数量
                loop.revindex	到循环结束的次数（从1开始）
                loop.revindex0	到循环结束的次数(从0开始）
            3.2.2.1. 迭代列表:
                {% for user in users %}
                    <li>{{ user.username|title }}</li>
                {% endfor %}
            3.2.2.2. 迭代字典:
                # 方式1: items()
                    {% for key, value in my_dict.items() %}
                        {{ key }} {{ value}}
                    {% endfor %}
                # 方式2: 迭代字典key，使用 my_dict.keys()
                    {% for key, value in my_dict.keys() %}
                        {{ key }} {{ value}}
                    {% endfor %}
                # 方式3: 迭代字典value，使用 my_dict.values()
                    {% for key, value in my_dict.values() %}
                        {{ key }} {{ value}}
                    {% endfor %}
                
    3.3. 注释: {# #}  eg: {# 我是注释 #} 

4. 过滤器: 变量可以通过“过滤器”进行修改，过滤器可以理解为是jinja2里面的内置函数和字符串处理函数。
    4.1. 使用方式: 只需要在变量后面使用管道(|)分割，多个过滤器可以链式调用，前一个过滤器的输出会作为后一个过滤器的输入。eg: {{ 'abc' | captialize  }}
    4.2. 常用的过滤器有:
            safe	 渲染时值不转义
            capitialize	 把值的首字母转换成大写，其他子母转换为小写  TODO 不存在？
            lower	 把值转换成小写形式 
            upper	 把值转换成大写形式 
            title	 把值中每个单词的首字母都转换成大写
            trim	 把值的首尾空格去掉
            striptags	 渲染之前把值中所有的HTML标签都删掉
            join 	 拼接多个值为字符串
            replace	 替换字符串的值
            round	 默认对数字进行四舍五入，也可以用参数进行控制
            int 	 把值转换成整型
            
5. 宏: 宏类似于Python中的函数，我们在宏中定义行为，还可以进行传递参数，就像Python中的函数一样一样儿的。
　　在宏中定义一个宏的关键字是 macro，后面跟其 宏的名称 和 参数 等。
    # 定义: 
        {% macro input(name,age=18) %}   # 参数age的默认值为18
            <input type='text' name="{{ name }}" value="{{ age }}" >
        {% endmacro %}
    # 调用方法也和Python的类似: 
        <p>{{ input('daxin') }} </p>
        <p>{{ input('daxin',age=20) }} </p>

6. 继承和Super函数: TODO
    模板继承。模板继承允许我们创建一个基本(骨架)文件，其他文件从该骨架文件继承，然后针对自己需要的地方进行修改。
　　jinja2的骨架文件中，利用block关键字表示其包涵的内容可以进行修改。 
            
"""

# 字符串模板字符内容
template = """hostname {{ hostname }}

no ip domain lookup
ip domain name local.lab
ip name-server {{ name_server_pri }}
ip name-server {{ name_server_sec }}

ntp server {{ ntp_server_pri }} prefer
ntp server {{ ntp_server_sec }}"""

data = {
    "hostname": "core-sw-waw-01",
    "name_server_pri": "1.1.1.1",
    "name_server_sec": "8.8.8.8",
    "ntp_server_pri": "0.pool.ntp.org",
    "ntp_server_sec": "1.pool.ntp.org",
}
out = "   world big big close!"
user = {
    "userName": "lihua",
    "password": "12345678",
    "age": 100,
}
users = [user, {"userName": "木木", "password": "88888888", "age": 999}]

my_dict = {
    "name": "GigabitEthernet1/1",
    "ip_address": "10.0.0.1/31",
    "description": "Uplink to core",
    "speed": "1000",
    "duplex": "full",
    "mtu": "9124"
}

# 1.1 创建字符串模板
strTemplate = Template(template)
print(strTemplate.render(data))

# 1.2. 创建带有数据的文件模板
# 1.2.1. 创建一个加载器对象，指定模板文件所在的目录
loader = FileSystemLoader('F:\Code\PythonSpace\study_python\py_study_test\study_library\jinjia2', encoding='gbk')
# 1.2.2. 创建一个环境对象，指定加载器
env = Environment(loader=loader)
# 1.2.3. 通过环境对象获取模板
template = env.get_template('test.template')

age = 9999
# 2. 渲染模板
result = template.render(out=out, users=users, my_dict=my_dict, user=user, age=age)

# 写入文件中
domainfile = open('F:\Code\PythonSpace\study_python\py_study_test\study_library\jinjia2\demo.txt', 'wb')
domainfile.write(result.encode('utf8'))
domainfile.flush()
domainfile.close()
