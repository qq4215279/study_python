from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

"""
爬虫库
抓取类：
1. urllib(Python3),自带的库。
解析类：
2. re：正则表达式官方库，不仅仅是学习爬虫要使用，在其他字符串处理或者自然语言处理的过程中，这是绕不过去的一个库，强烈推荐掌握。
综合类：
3. selenium：所见即所得式爬虫。综合了抓取和解析两种功能，一站式解决。
4. scrapy：另一个爬虫神器，适合爬取大量页面，甚至对分布式爬虫提供了良好的支持。强烈推荐。
"""

"""
使用selenium
1. 需要先下载 chromedriver.exe （与自己的谷歌浏览器版本相同）
    - 在Chrome浏览器地址栏中输入 chrome://version/
    - 下载 chromedriver.exe   => 下载地址  http://chromedriver.storage.googleapis.com/index.html
2.     

"""

# 用代码打开一个浏览器
# 尝试传参
path = r"D:\Install\App\Google安装\chromedriver.exe"
browser = webdriver.Chrome(executable_path=path)

# 在地址栏输入地址
browser.get('https://www.baidu.com')

# 找到输入框
search = browser.find_element("id", 'kw')
# 模拟输入框输入内容
search.send_keys("美女")

# 找到百度一下按钮
button = browser.find_element("id", 'su')
# 点击一下按钮
button.click()
time.sleep(2)

# 截图预览
browser.get_screenshot_as_file('截图.png')

# 打印当前页面的html内容
print(browser.page_source)

"""

"""

with open('baidu.html', 'w', encoding='utf-8') as f:
    f.write(browser.page_source)  # 包含redner+ajax

# 关闭浏览器
browser.close()
