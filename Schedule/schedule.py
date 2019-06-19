#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-19 10:45
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   None
"""
import aiohttp
import asyncio
import time

from multiprocessing import Process
from aiohttp import ServerDisconnectedError, ClientResponseError, ClientConnectorError
from DB.DBClient import *
from Util.error import ResourceDepletionError
from ProxyGetter.getFreeProxy import *
from Config.ConfigGetter import config

class ValidityTester(object):

    test_api = config.get_test_api

    def __init__(self):
        # 代理list
        self._raw_proxies = None
        # 可用代理list
        self._usable_proxies = []
        self._conn = DBClient()

    def set_raw_proxies(self, proxies):
        """
        设置代表list
        :param proxies:
        :return:
        """
        self._raw_proxies = proxies

    async def test_single_proxy(self, proxy):
        """
        异步检测单个代理，若有效，放入_usable_proxies
        :param proxy:
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        # 对取出的代理进行转码
                        proxy = proxy.decode('utf-8')

                    # 拼接代理地址
                    real_proxy = 'http://' + proxy
                    print(u'测试ip: ', proxy)
                    async with session.get(config.get_test_api, proxy=real_proxy,
                                           timeout=config.get_proxy_timeout) as response:
                        if response.status == 200:
                            # 测试通过，入库
                            self._conn.put(proxy)
                            print(u'有效IP: ', proxy)
                except (ProcessLookupError, TimeoutError, ValueError) as e:
                    print(u'无效IP:', proxy)
                    print(str(e))
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as e:
            print(str(e))

    def test(self):
        """
        aio 测试所有代理
        :return:
        """
        print(u'ValidityTester is working...')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError as e:
            print(u'Async Error')
            print(str(e))


class PoolAdder(object):
    """
    添加代理到代理池
    """

    def __init__(self, threshould):
        self._threshold = threshould
        self._conn = DBClient()
        self._tester = ValidityTester()
        self._crawler = GetFreeProxy()

    def is_over_threshold(self):
        """
        判断当前代理个数是否达到上限
        :return:
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print(u'PoolAdder is working...')
        proxy_count = 0

        while not self.is_over_threshold():
            # 取出属性列表中的所有方法
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # 测试爬虫代理
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP数量达到上限')
                    break
                if proxy_count == 0:
                    raise ResourceDepletionError


class Schedule(object):

    @staticmethod
    def valid_proxy(cycle=config.get_valid_check_cycle):
        """
        取出库中一半代理进行验证
        :param cycle:
        :return:
        """
        conn = DBClient()
        tester = ValidityTester()

        with True:
            print(u'Refreshing ip')
            count = int(0.5 * conn.queue_len)

            while count == 0:
                print('代理池无IP')
                time.sleep(cycle)
                continue

            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=config.get_pool_lower_threshold,
                   upper_threshold=config.get_pool_upper_threshold,
                   cycle=config.get_valid_check_cycle):
        """
        如果IP数量小于下限数量，则添加代理
        :param lower_threshold:
        :param upper_threshold:
        :param cycle:
        :return:
        """

        conn = DBClient()
        adder = PoolAdder(upper_threshold)

        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        print(u'Ip processing running...')
        # 开启从数据库拿IP进行检查的线程
        valid_process = Process(target=Schedule.valid_proxy)
        # 开启抓取IP并存储的线程
        check_process = Process(target=Schedule.check_pool)

        # 启动进程
        valid_process.start()
        check_process.start()
