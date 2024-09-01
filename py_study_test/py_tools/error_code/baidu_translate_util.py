# encoding: utf-8

import requests
import random
from hashlib import md5

APPID = '20240104001930626'
APPKEY = 'C_UBeh8GC64SQGpjOdEG'

"""
中文简体 -> 英文
"""


def translate_to_english(chinese_text):
    return do_translate(chinese_text)


"""
中文简体 -> 中文繁体
"""


def translate_to_tw(chinese_text):
    return do_translate(chinese_text, to_lang='cht')


"""
do 翻译
"""


def do_translate(world: str, from_lang='zh', to_lang='en') -> str:
    salt = random.randint(32768, 65536)
    sign = __make_md5(APPID + world + str(salt) + APPKEY)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': APPID, 'q': world, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(__get_url(), params=payload, headers=headers)
    result = r.json()

    # Show response
    # jsonStr = json.dumps(result, indent=4, ensure_ascii=False)
    # print(jsonStr)

    print("    ", result["trans_result"][0]["dst"])
    return result["trans_result"][0]["dst"]


# Generate salt and sign
def __make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


# 获取url
def __get_url():
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    return endpoint + path
