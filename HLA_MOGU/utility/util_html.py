# -*- coding: utf-8 -*-
import requests
from lxml import etree

from logs import logger
from utility.util_constant import request_timeout
from utility.util_user_agent import get_random_user_agent


def get_page_source(url, use_proxy=False, proxies=None):
    page_source = ''
    headers = {'User-Agent': get_random_user_agent()}
    try:
        if use_proxy:
            response = requests.get(url, headers=headers, timeout=request_timeout, proxies=proxies)
            page_source = response.text
        else:
            response = requests.get(url, headers=headers, timeout=request_timeout)
            page_source = response.text
        return page_source
    except Exception as e:
        logger.exception(e)
        if proxies:
            message = 'proxy {} is no longer in force'.format(proxies.get('https'))
            logger.info(message)
    return page_source


def get_tree(page_source):
    tree = etree.HTML(page_source)
    return tree
