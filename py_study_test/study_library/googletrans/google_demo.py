# encoding: utf-8
from googletrans import Translator
import requests
from httpcore import SyncHTTPProxy

proxies = {
    'http': 'http://127.001:33210',
    'https': 'http://127.0.0.1:33210'
}

# http_proxy = SyncHTTPProxy((b'http', b'127.001', 33210, b''))
# proxies = {'http': http_proxy, 'https': http_proxy}


def translate_to_english(chinese_text):
    translator = Translator(service_urls=['translate.google.cn'], proxies=proxies)
    result = translator.translate(text=chinese_text, src='zh-CN', dest='en')
    return result.text


# chinese_text = input('请输入中文句子：')
chinese_text = '中文'
english_text = translate_to_english(chinese_text)
print('翻译结果：', english_text)

# translator = Translator(service_urls=['translate.google.cn'], proxies=proxies)
# text = 'Hello, world!'
# result = translator.translate(text, dest='zh-CN')
# print(result.text)
