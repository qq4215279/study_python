import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

d = DesiredCapabilities.CHROME
chrome_options = Options()
# 使用无头浏览器
chrome_options.add_argument('--headless')
chrome_options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
# 浏览器启动默认最大化
chrome_options.add_argument("--start-maximized");
# 该处替换自己的chrome驱动地址
browser = webdriver.Chrome(r"D:\Install\App\Google安装\chromedriver.exe", options=chrome_options, desired_capabilities=d)
browser.set_page_load_timeout(150)
browser.get("https://daxue.163.com/find/enroll-data")
# 静态资源链接存储集合
urls = []
# 获取静态资源有效链接
for log in browser.get_log('performance'):
    if 'message' not in log:
        continue
    log_entry = json.loads(log['message'])
    try:
        # 该处过滤了data:开头的base64编码引用和document页面链接
        if "data:" not in log_entry['message']['params']['request']['url'] and 'Document' not in \
                log_entry['message']['params']['type']:
            urls.append(log_entry['message']['params']['request']['url'])
    except Exception as e:
        pass
print(urls)
