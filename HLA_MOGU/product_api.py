# -*- coding: utf-8 -*-
import re
import sys

import requests

from logs import logger
from utility.util_html import get_tree
from utility.util_csv import write_to_csv
from utility.util_read_cookie import read_cookie
from utility.util_constant import muji_search_url, file_path_1, cookie_path

headers = {
    'Cookie': read_cookie(cookie_path),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.77 Safari/537.36',
    }


def get_category_info(_url):
    """
    获取产品信息
    :param _url: 综合查询链接
    :return: category_info_list: [[category_name, api], [], ...]
    """
    category_info_list = []
    response = requests.get(_url, headers=headers)
    html = response.text
    if not html:
        logger.critical('{}请求失败，请手动检查是否要登录'.format(_url))
        sys.exit()
    tree = get_tree(html)
    xpath_expr = '//a[@class="cat-name fst-cat-name"]'
    result = tree.xpath(xpath_expr)
    if not result:
        logger.critical('在按综合查询页面没有找到产品')
        logger.critical('请手动检查网址是否错误，{}'.format(_url))
        sys.exit()
    for _ in result:
        category_name = _.xpath('text()')
        category_api = _.xpath('@href')
        if not category_name or not category_api:
            continue
        name = category_name[0]
        api = category_api[0]
        if name == '服装' or name == '所有宝贝':
            continue
        category_info_list.append([name, api])
    return category_info_list


def clean_out_category_info(lst):
    """
    清洗产品信息，从api里提取产品ID，构造新的列表
    :param lst: category_info_list
    :return: category_info_list_cleaned: [[category_name, category_id, api], [], ...]
    """
    category_info_list_cleaned = []
    pat = re.compile(r'category-(\d+).*')
    for _ in lst:
        category_name = _[0]
        api = _[1]
        # 如果需要按综合分类下所有产品的api，就添加下面这行
        # api = 'https:' + api
        if pat.findall(api):
            category_id = pat.findall(api)[0]
            category_info_list_cleaned.append([category_name, category_id])
    write_to_csv(category_info_list_cleaned, file_path_1)


def main_product():
    category_info = get_category_info(muji_search_url)
    clean_out_category_info(category_info)


if __name__ == '__main__':
    main_product()
