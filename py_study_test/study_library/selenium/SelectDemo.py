from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# 家里
path = r"D:\Install\App\Google安装\chromedriver.exe"
url = 'D:\Code\PythonWorkSpace\study_python\py_study_test\study_library\selenium\帅哥.html'
# 公司
# path = r"D:\Install\Google\chromedriver.exe"
# url = 'D:\data\code\pythonWorkSpace\study_python\py_study_test\study_library\selenium\帅哥.html'

browser = webdriver.Chrome(executable_path=path)

browser.get(url)
time.sleep(2)

name = browser.find_element(By.NAME, "请选择帅哥")

# 根据索引选择
Select(name).select_by_index("2")
time.sleep(2)

# 根据value值选择
Select(name).select_by_value("草儿")
time.sleep(2)

# 根据文本值选择
Select(name).select_by_visible_text("才哥")
time.sleep(2)

# 关闭浏览器
browser.close()