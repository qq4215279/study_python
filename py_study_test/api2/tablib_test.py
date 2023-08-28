# coding:utf-8

import json
import tablib

def getData():
    dataset1 = tablib.Dataset()
    dataset1.headers = ['id', 'name', 'age', 'sex']
    dataset1.append(['1', '朱宇', '21', 'male'])
    dataset1.append(['2', '张昊', '22', 'male'])
    dataset1.append(['1', '伍洋', '20', 'male'])

    # dataset1.xls  # 转成xls格式

    open('./file/testXLS.xls', 'wb').write(dataset1.xls)

if __name__ == '__main__':
    getData()