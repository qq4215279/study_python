# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from selenium.webdriver import ChromeOptions
import time
import json


path = r"D:\Install\Google\chromedriver.exe"
s = Service(path)

opt = Options()
opt.add_experimental_option('excludeSwitches', ['enable-automation'])
opt.add_argument('--headless')

# browser = webdriver.Chrome(service=s, options=opt)
browser = webdriver.Chrome(service=s)

# 打开江西教育考试院
browser.get('http://www.jxeea.cn/col/col26681/index.html')

time.sleep(2)

# year = browser.find_element(By.XPATH, '//*[@id="year"]')
year = browser.find_element(By.ID, 'year')
# 根据索引选择
Select(year).select_by_index("0")

klmc = browser.find_element(By.XPATH, '//*[@id="klmc"]')
# 根据索引选择
Select(klmc).select_by_index("1")

pcmc = browser.find_element(By.XPATH, '//*[@id="pcmc"]')
# 根据索引选择
Select(pcmc).select_by_index("2")

time.sleep(20)

browser.close()