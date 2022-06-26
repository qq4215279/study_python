import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#caps = DesiredCapabilities.CHROME
#caps['loggingPrefs'] = {'performance': 'ALL'}
# 78版本的chrome需要加这个，https://stackoverflow.com/questions/56812190/protractor-log-type-performance-not-found-error
# caps = {
#     'browserName': 'chrome',
#     'loggingPrefs': {
#         'browser': 'ALL',
#         'driver': 'ALL',
#         'performance': 'ALL',
#     },
#     'goog:chromeOptions': {
#         'perfLoggingPrefs': {
#             'enableNetwork': True,
#         },
#         'w3c': False,
#     },
# }

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

path = r"D:\Install\Google\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path, desired_capabilities=caps)

driver.get('https://www.baidu.com')

logs = [json.loads(log['message'])['message'] for log in driver.get_log('performance')]

with open('devtools.json', 'wb') as f:
    json.dump(logs, f)

driver.close()
