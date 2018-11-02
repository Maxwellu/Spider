# -*- coding: utf-8 -*-
import re
import sys
import json
import time
from multiprocessing import Queue

import requests

from logs import logger
from utility.util_constant import request_timeout
from utility.util_user_agent import get_random_user_agent
from utility.util_constant import add_white_list_api, local_host_api
from utility.util_constant import proxy_api, proxy_interval, proxy_use_count, proxy_queue_max, get_white_list_api

producer_queue = Queue()
mark_proxy_use_queue = Queue()
headers = {'User-Agent': get_random_user_agent(),
           'Connection': 'keep-alive',
           }


def get_localhost_ip(_url):
    """
    百度搜索本地IP
    :param _url:
    :return:
    """
    try:
        response = requests.get(_url, headers=headers, timeout=request_timeout)
        html = response.text
        pat = re.compile('本机IP:&nbsp;([0-9|.]+)')
        result = pat.findall(html)
        if result:
            localhost = result[0]
            return localhost
    except Exception as e:
        logger.exception(e)


def get_white_list(_url):
    api_list = []
    try:
        response = requests.get(_url, headers=headers, timeout=request_timeout)
        _api_list = json.loads(response.text)
        api_list = _api_list.get('msg')
    except Exception as e:
        logger.exception(e)
    return api_list


def add_white_list(_url, ip):
    """
    将本地IP添加到白名单列表
    :param _url: 添加白名单接口
    :param ip: 本地IP
    :return: None
    """
    api = _url + ip
    try:
        response = requests.get(api, headers=headers, timeout=request_timeout)
        logger.info(response.text)
    except Exception as e:
        logger.exception(e)


def gen_one_proxy():
    # url仅仅适用蘑菇代理
    url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?' \
          'appKey=cd9d62da3f9442bcbcbc5f9158acfd00&count=1&expiryDate=1&format=1&newLine=2'
    res = requests.get(url, headers=headers, timeout=10)
    html = res.text
    if 'port' in html and 'ip' in html:
        return True
    else:
        return False


def charge_white_list():
    """
    添加本地IP到ET代理白名单列表
    :return: None
    """
    # 百度查找IP
    localhost_ip = get_localhost_ip(local_host_api)
    api_list = get_white_list(get_white_list_api)
    if localhost_ip in api_list:
        logger.info('{} is already in api list'.format(localhost_ip))
        return
    count = 0
    # 添加白名单
    while True:
        add_white_list(add_white_list_api, localhost_ip)
        count += 1
        if gen_one_proxy():
            logger.info('添加白名单成功')
            return
        if count >= 5:
            logger.warning('添加白名单失败，请手动添加')
            return


def get_json(url):
    _json = ''
    try:
        response = requests.get(url, headers=headers, timeout=request_timeout)
        _json = json.loads(response.text)
    except Exception as e:
        logger.exception(e)
    return _json


def get_data_list(_json):
    if not _json:
        return False, False
    if _json.get('code') == '3001':
        logger.warning('提取频繁请按照规定频率提取!')
        return False, False
    if _json.get('code') == '3006':
        logger.warning('提取数量用完!')
        mark_proxy_use_queue.put(1)
        return False, True
    if _json.get('code') != '0':
        return False, False
    _data_list = _json.get('msg')
    return _data_list, False


def put_ip_to_queue(data_list):
    if not data_list:
        return
    for data in data_list:
        ip = data.get('ip')
        port = data.get('port')
        proxy = ip + ':' + port
        logger.info('proxy {} is ready insert to queue'.format(proxy))
        for _ in range(proxy_use_count):
            # 每一个代理使用几次,由proxy_use_count配置
            producer_queue.put_nowait(proxy)


def proxy_main():
    _platform = sys.platform
    while True:
        # 如果不是macOS操作系统就可以调用进程通信队列的qsize方法
        if 'darwin' not in _platform:
            if producer_queue.qsize() >= proxy_queue_max:
                continue
        _json = get_json(proxy_api)
        data_list, is_used = get_data_list(_json)
        # 代理API使用完就不再向代理接口发送请求
        if is_used:
            break
        # 如果没有获取到IP，重新请求
        if not data_list:
            continue
        put_ip_to_queue(data_list)
        time.sleep(proxy_interval)
    logger.info('今日可用IP已经全部提取完/商品全部爬完, 已经不需要再去请求代理')


def empty_queue(_queue):
    """
    情况队列
    :param _queue:
    :return:
    """
    while not _queue.empty():
        _queue.get()


if __name__ == '__main__':
    charge_white_list()
    # proxy_main()
    # get_white_list(get_white_list_api)
