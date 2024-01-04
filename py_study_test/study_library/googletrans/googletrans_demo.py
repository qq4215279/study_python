# encoding: utf-8
import json
import urllib

from translate import Translator
import random

user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0)']


def translate_content_ch():
    # 实现英文转中文
    translator = Translator(to_lang='chinese')

    # translator._session.headers['User-Agent'] = random.choice(user_agents)

    translation = translator.translate('hello')
    return translation


def translate_content_en():
    # 实现中文转英文
    translator = Translator(from_lang='chinese', to_lang='english')
    translation = translator.translate("公告")
    return translation


def translate_to_simplified_chinese(traditional_chinese_text):
    translator = Translator(from_lang="zh-CN", to_lang="zh-TW")
    translation = translator.translate(traditional_chinese_text)
    return translation


# print(translate_content_ch())

# print(translate_content_en())

# print(translate_to_simplified_chinese("刘振"))


def translate_to_english(chinese_text):
    translator = Translator(service_urls=['translate.google.cn'])
    result = translator.translate(chinese_text, dest='en')
    return result.text

chinese_text = input('请输入中文句子：')
english_text = translate_to_english(chinese_text)
print('翻译结果：', english_text)