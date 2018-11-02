# -*- coding: utf-8 -*-
import re
import time
from queue import Queue
from random import randint

import requests

from logs import logger
from utility.util_html import get_tree
from utility.util_send_email import SendMail
from utility.util_read_cookie import read_cookie
from utility.util_csv import read_from_csv, write_to_csv
from utility.util_constant import file_path_1, file_path_2, cookie_path, error_url

url_all = []
sleep_range = [60, 120]
category_queue = Queue()
category_page_queue = Queue()
cookie = read_cookie(cookie_path)
pat_id = re.compile(r'id=(\d+)&rn=')  # 从url提取商品ID
pat = re.compile(r'ui-page-s-len.*?>(\d*/\d*)</b>')  # 商品页数正则表达式
# 测试保存品类是否正常的API
test_url = 'https://muji.tmall.com/i/asynSearch.htm?_ksTS=1540869520061_122&callback=jsonp123&' \
               'mid=w-14901419059-0&wid=14901419059&tsearch=y&orderType=defaultSort&catId=910220788&scid=910220788'
headers = {
    'Cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.77 Safari/537.36',
    }


def get_merchandise_api(category, category_id, default_page=1):
    """
    :param category: 产品中文名，如女装，男装等
    :param category_id: 产品ID
    :param default_page: 默认第一页
    :return:
    """
    category_api = 'https://muji.tmall.com/i/asynSearch.htm?_ksTS=1540869520061_122&' \
                   'callback=jsonp123&mid=w-14901419059-0&wid=14901419059&tsearch=y&' \
                   'orderType=defaultSort&catId={}&pageNo={}&scid={}'.format(category_id, default_page, category_id)
    res = requests.get(category_api, headers=headers)
    html = res.text
    page_result = pat.findall(html)
    if not page_result:
        logger.info(page_result)
        return
    pages = page_result[0].split('/')[-1]
    pages = int(pages)
    logger.info('{}共有{}页，正在爬取第{}页'.format(category, pages, default_page))

    xpath_expr = '//div[contains(@class,"J_TItems")]/div'
    tree = get_tree(html)
    xpath_result = tree.xpath(xpath_expr)
    if not xpath_result:
        return
    for _ in xpath_result:
        merchandise_url = _.xpath('./dl/dd[2]/a/@href')
        merchandise_title = _.xpath('./dl/dd[2]/a/text()')
        if not merchandise_title or not merchandise_url:
            continue
        merchandise_url = ['https:' + _[2:-2] for _ in merchandise_url]
        merchandise_title = [_.strip() for _ in merchandise_title]
        merchandise_id = []
        for url in merchandise_url:
            _res = pat_id.findall(url)
            if not _res:
                continue
            _id = _res[0]
            merchandise_id.append(_id)

        id_title_url_list = list(zip(merchandise_id, merchandise_title, merchandise_url))
        id_title_url_list = [list(_) for _ in id_title_url_list]
        merchandise_url.clear()
        merchandise_title.clear()
        merchandise_id.clear()

        for _ in id_title_url_list:
            _.insert(0, category_id)
            _.insert(0, category)
            url_all.append(_)

        id_title_url_list.clear()
    logger.info('{}的第{}页爬取完成！'.format(category, default_page))
    return pages


def try_get_asynearch():
    try:
        response = requests.get(test_url, headers=headers)
        html = response.text
        if '上一页' in html:
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
    return


def repeat_login():
    while True:
        logger.info('请手动登录天猫账号并把cookie保存到cookie.txt文件中')
        if try_get_asynearch():
            logger.info('cookie有效')
            break
        else:
            logger.info('cookie无效，请重新登录后再获取一次')
            title = '登录异常'
            message = 'cookie无效，请重新登录，登录后请手动访问网址{}看网页是否正常，若登录正常，该网址异常，请重新抓包，' \
                      '如果未登录账号，你将会看到类似如下的内容：{}'.format(test_url, error_url)
            obj = SendMail(title, message)
            obj.send_mail()
        # 每隔30分钟读取cookie.txt配置文件
        time.sleep(1800)


def main_merchandise_url():
    product_list = read_from_csv(file_path_1)
    for _ in product_list:
        category_queue.put(_)
    product_list.clear()

    while not category_queue.empty():
        _ = category_queue.get()
        category = _[0]
        category_id = _[1]
        logger.info('开始爬取产品-->"{}"，它的ID是: {}'.format(category, category_id))
        total_page = get_merchandise_api(category, category_id)
        if not total_page:
            logger.info('请先手动确认网址{}是否可以访问并返回数据，如果看到形如：{}则表示cookie失效'.format(test_url, error_url))
            logger.info('产品"{}"爬取失败，爬取太频繁，请重新登录后再爬'.format(category))
            logger.info('产品{}重新放入队列，等待后续重新爬取'.format(category))
            category_queue.put(_)
            title = '警告'
            message = '爬取太频繁，请重新登录'
            obj = SendMail(title, message)
            obj.send_mail()
            # 尝试重新登录账号
            repeat_login()
            continue
        if total_page <= 1:
            random_sleep_time = randint(sleep_range[0], sleep_range[1])
            logger.info('休息{}秒后再爬下一个产品吧！'.format(random_sleep_time))
            time.sleep(random_sleep_time)
            continue
        else:
            random_sleep_time = randint(sleep_range[0], sleep_range[1])
            logger.info('休息{}秒后再爬"{}"的下一页吧！'.format(random_sleep_time, category))
            time.sleep(random_sleep_time)

        for i in range(2, total_page + 1):
            pages = get_merchandise_api(category, category_id, i)
            if not pages:
                logger.info('请先手动确认网址{}是否可以访问并返回数据，如果看到形如：{}则表示cookie失效'.format(test_url, error_url))
                logger.info('产品"{}"的第{}页爬取失败，将该页及其后面所有页先加入队列等待后续爬取'.format(category, i))
                for _ in range(i, total_page + 1):
                    category_page_queue.put([category, category_id, _])
                break
            if i < total_page:
                random_sleep_time = randint(sleep_range[0], sleep_range[1])
                logger.info('休息{}秒后再爬"{}"的下一页吧！'.format(random_sleep_time, category))
                time.sleep(random_sleep_time)
            else:
                random_sleep_time = randint(sleep_range[0], sleep_range[1])
                logger.info('"{}"全部爬完，休息{}秒后再爬下一个产品吧！'.format(category, random_sleep_time))
                time.sleep(random_sleep_time)
        logger.info('*' * 50)

    if category_page_queue.empty():
        logger.info('所有产品爬取完毕，准备写入文件！')
        write_to_csv(url_all, file_path_2)
        url_all.clear()
        return

    logger.info('现在开始爬取之前请求某个产品时某一页获取失败的情况！')
    while not category_page_queue.empty():
        _ = category_page_queue.get()
        category = _[0]
        category_id = _[1]
        page = _[-1]
        total_page = get_merchandise_api(category, category_id, page)
        if not total_page:
            category_page_queue.put(_)
            logger.info('请先手动确认网址{}是否可以访问并返回数据，如果看到形如：{}则表示cookie失效'.format(test_url, error_url))
            logger.info('产品"{}"的第{}页爬取失败，爬取太频繁，请重新登录后再爬'.format(category, page))
            logger.info('产品"{}"的第{}页重新放入队列，等待后续重新爬取'.format(category, page))
            title = '警告'
            message = '爬取太频繁，请重新登录'
            obj = SendMail(title, message)
            obj.send_mail()
            # 尝试重新登录账号
            repeat_login()
        random_sleep_time = randint(sleep_range[0], sleep_range[1])
        logger.info('休息{}秒后再爬下一个吧！'.format(random_sleep_time))
        time.sleep(random_sleep_time)

    logger.info('所有产品爬取完毕，准备写入文件！')
    write_to_csv(url_all, file_path_2)
    url_all.clear()


if __name__ == '__main__':
    repeat_login()
    # main_merchandise_url()
    # get_merchandise_api('活动特辑', '910227400')
