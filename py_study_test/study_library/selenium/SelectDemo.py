from selenium import webdriver
from selenium.webdriver.support.select import Select
import time


path = r"D:\Install\App\Google安装\chromedriver.exe"
browser = webdriver.Chrome(executable_path=path)

url = 'D:\Code\PythonWorkSpace\study_python\py_study_test\study_library\selenium\帅哥.html'
browser.get(url)
time.sleep(2)

# 根据索引选择
Select(browser.find_element_by_name("帅哥")).select_by_index("2")
time.sleep(2)
# 根据value值选择
Select(browser.find_element_by_name("帅哥")).select_by_value("草儿")
time.sleep(2)
# 根据文本值选择
Select(browser.find_element_by_name("帅哥")).select_by_visible_text("才哥")
time.sleep(2)

# 关闭浏览器
browser.close()