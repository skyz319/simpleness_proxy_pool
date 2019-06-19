#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-18 15:59
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   启动Flask,网页API
"""
from flask import Flask, g
from DB.DBClient import *

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    """
    如果没有数据库连接，则打开一个新的连接
    :return: 
    """
    if not hasattr(g, 'redis_client'):
        g.redis_client = DBClient()

    return g.redis_client


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/get')
def get_proxy():
    """
    获取一个代理IP
    :return:
    """
    conn = get_conn()
    return conn.pop()


@app.route('/count')
def get_counts():
    """
    获取当前代理池IP总数
    :return:
    """
    conn = get_conn()
    return str(conn.queue_len)


if __name__ == '__main__':
    app.run()
