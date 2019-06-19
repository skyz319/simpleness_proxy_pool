#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019-06-18 16:47
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   抓取免费代理
"""
import re
import urllib3

from Util.WebRquest import WebRequest
from Util.utilFunction import getHtmlTree

# 消除警告信息
urllib3.disable_warnings()


class ProxyMetaclass(type):
    """
    元类，在当前类加入__CrawlFunc__和__CrawlFuncCount__
    两个参数，分别表示爬虫函数，和爬虫函数的数量
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        """
        动态添加属性
        """
        attrs['__CrawlFunc__'] = []

        # 将所有指定开头的方法添加到列表
        for k, v in attrs.items():
            if 'free_proxy_wall_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1

        attrs['__CrawlFuncCount__'] = count

        return type.__new__(cls, name, bases, attrs)


class GetFreeProxy(object, metaclass=ProxyMetaclass):
    """
    获取免费代理
    """
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback: ', callback)
        """
        动态执行指定命令
        """
        for proxy in eval('self.{}()'.format(callback)):
            print('Getting ', proxy, 'from ', callback)
            proxies.append(proxy)

        return proxies

    def free_proxy_wall_ip66(self, count=40):
        """
        代理66 http://www.66ip.cn/
        :param count: 提取数量
        :return:
        """
        urls = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={count}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={count}"
            "&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip",
        ]
        request = WebRequest()
        for _ in urls:
            url = _.format(count=count)
            # html = request.get(url).content
            html = request.get_page(url)
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html)
            for ip in ips:
                yield ip.strip()

    def free_proxy_wall_xici(self, page_count=1):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    def free_proxy_wall_goubanjia(self):
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                            and not(contains(@style, 'display:none'))
                                            and not(contains(@class, 'port'))
                                            ]/text()
                                    """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass


    def free_proxy_wall_kuaidaili(self):
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    def free_proxy_wall_ip3366(self):
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    # def free_proxy_wall_iphai(self):
    #     """
    #     IP海 http://www.iphai.com/free/ng
    #     :return:
    #     """
    #     urls = [
    #         'http://www.iphai.com/free/ng',
    #         'http://www.iphai.com/free/np',
    #         'http://www.iphai.com/free/wg',
    #         'http://www.iphai.com/free/wp'
    #     ]
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
    #                              r.text)
    #         for proxy in proxies:
    #             yield ":".join(proxy)

    def free_proxy_wall_jianxianli(self, page_count=2):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    # def free_proxy_wall_cnproxy(self):
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # def free_proxy_wall_proxylist(self):
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    def free_proxy_wall_listplus(self):
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


if __name__ == '__main__':
    pass
