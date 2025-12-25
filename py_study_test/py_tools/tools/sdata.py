#!/usr/bin/env python
#-*- encoding:utf8-*-

#  Copyright 2018-2021,上海哈里奥网络科技有限公司
#  All Right Reserved.

import sdata_pack as dbdeploy
import os, sys

# 打包静态数据库
db = "cehua_sbtj_cn_sdata"
path = "D:\\data\\sbtj\\sdata\\"
version = "1.0.0.0"




#dbdeploy.db_dump_xml_path(sys.argv[1], sys.argv[2], sys.argv[3])
dbdeploy.pack(
    host='10.9.200.244', # 10.5.201.56
    user='root', 
    password='qwert',    # 1234
    db=db, 
    path=path, 
    version=version)
