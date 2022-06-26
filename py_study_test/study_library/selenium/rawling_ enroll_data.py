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
"""

caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}

url = "https://daxue.163.com/find/enroll-data"

path = r"D:\Install\Google\chromedriver.exe"
# browser = webdriver.Chrome(executable_path=path)

# 尝试传参 https://blog.csdn.net/sinat_29957455/article/details/122242196
# # s = Service("chromedriver.exe")
s = Service(path)
# browser = webdriver.Chrome(service=s)



# 加载cookies中已经保存的账号和密码
# C:\Users\liuzhen\AppData\Local\Google\Chrome\Application\chrome.exe -remote-debugging-port=9222 --user-data-dir="C:\Users\liuzhen\AppData\Local\Google\Chrome\User Data"
options = ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(service=s, chrome_options=options, desired_capabilities=caps)
# browser = webdriver.Chrome(executable_path=path, chrome_options=options)

browser.get(url)
time.sleep(2)

print("--------------------------------->")

element = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/input')

print(element.id)
print(element.text)

element.send_keys("南昌大学")

#
# element2 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/div/div/i')
# element2.click()

action = ActionChains(browser)
one_click = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[1]/div/div/div/i')
action.click(one_click).perform()

time.sleep(2)


# 打印当前页面的html内容
# print(browser.page_source)

# with open('gaokao.html', 'w', encoding='utf-8') as f:
#     # 包含 redner + ajax
#     f.write(browser.page_source)

logs = [json.loads(log['message'])['message'] for log in browser.get_log('performance')]

with open('devtools.json', 'wb') as f:
    json.dump(logs, f)

browser.close()