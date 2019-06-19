#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ConfigGetter.py
@Time    :   2019/06/18 14:59:52
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   配置读取类
'''
from Util.utilClass import LazyProperty
from Config.Setting import *


class ConfigGetter(object):

    def __init__(self):
        pass

    @LazyProperty
    def db_table_name(self):
        return str(DB_TABLE_NAME)

    @LazyProperty
    def db_type(self):
        return str(DB_TYPE)

    @LazyProperty
    def db_host(self):
        return str(DB_HOST)

    @LazyProperty
    def db_port(self):
        return DB_PORT

    @LazyProperty
    def db_password(self):
        return str(DB_PASSWORD)

    @LazyProperty
    def get_test_api(self):
        return str(TEST_API)

    @LazyProperty
    def get_proxy_timeout(self):
        return GET_PROXY_TIMEOUT

    @LazyProperty
    def get_valid_check_cycle(self):
        return VALID_CHECK_CYCLE

    @LazyProperty
    def get_pool_len_check_cycle(self):
        return POOL_LEN_CHECK_CYCLE

    @LazyProperty
    def get_pool_lower_threshold(self):
        return POOL_LOWER_THRESHOLD

    @LazyProperty
    def get_pool_upper_threshold(self):
        return POOL_UPPER_THRESHOLD


config = ConfigGetter()


if __name__ == '__main__':
    print(config.db_type)
    print(config.db_host)
    print(config.db_port)
    print(config.db_password)
