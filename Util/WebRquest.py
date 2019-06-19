#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-18 16:49
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   网络请求类
"""
import requests
import time
from fake_useragent import UserAgent
from requests.models import Response


class WebRequest(object):
    def __init__(self):
        pass

    @property
    def header(self):
        ua = UserAgent()

        return {
            'User-Agent': ua.random,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
        }

    def get(self, url, header=None, retry_time=5, timeout=30,
            retry_flag=list(), retry_interval=5, **kwargs):
        """
        请求方法
        :param url: 目录Url
        :param header: headers
        :param retry_time: 网络错误的重试时间
        :param timeout: 超时时间
        :param retry_flag: 如果有内容，则重试其中内容
        :param retry_interval: 重试间隔（秒）
        :param args:
        :param kwargs:
        :return:
        """
        headers = self.header

        if header and isinstance(header, dict):
            headers.update(header)

        while True:

            try:
                html = requests.get(url=url, headers=headers, timeout=timeout, **kwargs)
                if any(f in html.content for f in retry_flag):
                    raise Exception
                return html

            except Exception as e:
                print(e)
                retry_time -= 1

                if retry_time <= 0:
                    # 多次请求失败
                    resp = Response()
                    resp.status_code = 200
                    return resp

                time.sleep(retry_interval)

    def get_page(self, url):

        ua = UserAgent()

        headers = {
            'User-Agent':  ua.random,
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        print('Getting', url)
        try:
            r = requests.get(url, headers=headers)
            print('Getting result', url, r.status_code)
            if r.status_code == 200:
                return r.text
        except ConnectionError:
            print('Crawling Failed', url)
            return None
