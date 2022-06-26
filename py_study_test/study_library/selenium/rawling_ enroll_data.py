from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver import ChromeOptions
import time
import json

"""
爬取2021江西高考录取数据
地址：https://daxue.163.com/find/enroll-data

尝试传参 https://blog.csdn.net/sinat_29957455/article/details/122242196
"""


url = "https://daxue.163.com/find/enroll-data"

# 家里
path = r"D:\Install\App\Google安装\chromedriver.exe"
# 公司
# path = r"D:\Install\Google\chromedriver.exe"


# 加载cookies中已经保存的账号和密码
# C:\Users\liuzhen\AppData\Local\Google\Chrome\Application\chrome.exe -remote-debugging-port=9222 --user-data-dir="C:\Users\liuzhen\AppData\Local\Google\Chrome\User Data"

s = Service(executable_path=path)
options = ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# browser = webdriver.Chrome(executable_path=path, chrome_options=options)
browser = webdriver.Chrome(service=s, chrome_options=options)

browser.get(url)
time.sleep(2)

print("--------------------------------->")
# //*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/input
element = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/input')
print('id: ', element.id)
print('text: ', element.text)
element.send_keys("东华理工大学")

# 单选
# time.sleep(3)
# browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[3]/div[2]/div/label[2]/span[1]/input').click()

# ==========> 下拉框
# name = browser.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]')
# 根据索引选择
# Select(name).select_by_index(1)
# Select(name).select_by_value("本科第二批")
# time.sleep(2)


# 搜索方式1  失败！！
# element2 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/div/div/i')
# element2.click()
# 搜索方式2  可用！
action = ActionChains(browser)
one_click = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/div/div/i')
action.click(one_click).perform()

time.sleep(2)

txt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[3]/div[2]/div/div').text
print("txt: ", txt)


# with open('gaokao.html', 'w', encoding='utf-8') as f:
#     # 包含 redner + ajax
#     f.write(browser.page_source)


# browser.close()