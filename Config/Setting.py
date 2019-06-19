#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ConfigGetter.py
@Time    :   2019/06/18 14:59:52
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   配置文件
'''


class ConfigError(BaseException):
    pass


# Redis数据库的地址和端口
DB_TABLE_NAME = 'proxies'
DB_TYPE = 'Redis'
DB_HOST = 'localhost'
DB_PORT = 6379

# 如果Redis有密码，则添加这句密码，否则设置为None或''
DB_PASSWORD = ''

# 获得代理测试时间界限
GET_PROXY_TIMEOUT = 9

# 代理池数量界限
POOL_LOWER_THRESHOLD = 20
POOL_UPPER_THRESHOLD = 1000

# 检查周期
VALID_CHECK_CYCLE = 60
POOL_LEN_CHECK_CYCLE = 20

# 测试API，用百度来测试
TEST_API = 'http://www.baidu.com'
