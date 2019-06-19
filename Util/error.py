#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-18 16:07
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   自定义错误
"""


class ResourceDepletionError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理源已用尽')


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池内没有数据')


