#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ConfigGetter.py
@Time    :   2019/06/18 14:59:52
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   DB工厂类
"""
import redis

from Util.utilClass import Singleton
from Util.error import PoolEmptyError
from Config.ConfigGetter import config


class DBClient(object):
    """
    DBClient DB工厂类，提供get/put/pop/len及flush方法
    """

    __metaclass__ = Singleton

    def __init__(self, host=config.db_host, port=config.db_port):
        """
        初始化数据库
        :param host:
        :param port:
        """
        if config.db_password:
            self._db = redis.Redis(host=host, port=port, password=config.db_password)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        从数据库中取出指定个数的代理IP
        :param count: IP的个数
        :return: 代理IP
        """
        # 返回指定区间同的元素，区间以偏移量 start 和 stop 指定。
        # lrange(key , start , stop)
        proxies = self._db.lrange(config.db_table_name, 0, count - 1)
        # 对一个列表进行修剪，只保留指定区间内的元素，其它删除
        # ltrim(key , start , stop)
        self._db.ltrim(config.db_table_name, count, -1)

        return proxies

    def put(self, proxy):
        """
        从列表右侧放入代理
        :param proxy: 代理IP
        :return:
        """
        # 将指定的一个或多个值插入到列表的表尾（最右侧）
        # rpush(key , value)
        self._db.rpush(config.db_table_name, proxy)

    def pop(self):
        """
        从列表右侧出栈一个IP
        :return:
        """
        try:
            return self._db.rpop(config.db_table_name).decode('utf-8')
        except PoolEmptyError:
            return 0

    @property
    def queue_len(self):
        """
        获取列表长度
        :return: 列表长度
        """
        # 返回列表的长度。 如果列表 key 不存在，则 key 被解释为一个空列表，返回 0 。 如果 key 不是列表类型，返回一个错误。
        # len(key)
        return self._db.llen(config.db_table_name)

    def flush(self):
        """
        删除列表中所有的数据
        :return: 删除结果
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = DBClient()
    print(conn.queue_len)
