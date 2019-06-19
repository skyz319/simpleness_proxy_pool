#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-19 10:09
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   None
"""
from ProxyGetter.getFreeProxy import GetFreeProxy
from Util.utilFunction import verifyProxyFormat

from Util.LogHandler import LogHandler

log = LogHandler('check_proxy', file=False)


class CheckProxy(object):

    def checkAllGetProxyFunc(self):
        """
        检查getFreeProxy所有代理获取函数的运行情况
        :return:
        """
        import inspect
        member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)
        proxy_count_dict = dict()

        for func_name, func in member_list:
            print(u'开始运行{}'.format(func_name))

            try:
                proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
                proxy_count_dict[func_name] = len(proxy_list)
            except Exception as e:
                print(u'代理获取函数 {} 运行出错！'.format(func_name))
                print(str(e))

        print(u'所有函数运行完毕' + ' ******' * 5)

        for func_name, func in member_list:
            print(u'函数 {n}, 获取到代理 {c}'.format(n=func_name, c=proxy_count_dict.get(func_name, 0)))


    @staticmethod
    def checkGetProxyFunc(func):
        """
        检查指定的getFreeProxy函数运行情况
        :param func:
        :return:
        """

        func_name = getattr(func, '__name__', 'None')
        print(u'开始运行函数：{}'.format(func_name))

        count = 0
        for proxy in func():

            if verifyProxyFormat(proxy):
                print(u'{} 获取到代理： {}'.format(func_name, proxy))
                count += 1

        print(u'函数 {n} 运行完毕，获取到 {c} 个代理。'.format(n=func_name, c=count))


if __name__ == '__main__':
    # CheckProxy.checkAllGetProxyFunc()
    CheckProxy.checkGetProxyFunc(GetFreeProxy.free_proxy_wall_xici)




