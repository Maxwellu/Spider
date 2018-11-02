# -*- coding: utf-8 -*-
import re

from logs import logger
from utility.util_html import get_page_source, get_tree
from utility.util_proxy import producer_queue, mark_proxy_use_queue

detail_all = list()


def list_to_string(lst, symbol=','):
    """
    将列表里的元素拼接成字符串
    :param lst: 列表[1, 2, 3, 4]
    :param symbol: 分隔符号
    :return: '1,2,3,4'
    """
    length = len(lst)
    count = length - 1
    for _ in range(count):
        lst.insert(2 * _ - 1, symbol)
    lst = ''.join(lst)
    return lst


def get_inventory(page_source):
    """
    :param page_source: 网页源代码
    :return: inventory: 库存
    """
    inventory = ''
    pat = re.compile(r'"quantity":(\d+),')
    result = pat.findall(page_source)
    if result:
        inventory = result[0]       
    return inventory


def get_monthly_sales_promotion_page_source(item_id, use_proxy=False, proxies=None):
    _url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{}%22%7D' \
           .format(item_id)
    page_source = get_page_source(_url, use_proxy, proxies)
    return page_source


def get_monthly_sales(page_source):
    """
    :param page_source: 月销量和促销价网页源代码
    :return: monthly_sales: 月销量
    """
    monthly_sales = ''
    if not page_source:
        return monthly_sales
    pat = re.compile(r'\\"sellCount\\":\\"(\d+)\\",')
    result = pat.findall(page_source)
    if result:
        monthly_sales = result[0]
    return monthly_sales


def get_promotion(page_source):
    """
    :param page_source: 月销量和促销价网页源代码
    :return: promotion: 促销价
    """
    promotion = ''
    if not page_source:
        return promotion
    pat = re.compile(r'\\"transmitPrice\\":{\\"priceText\\":\\"(\d+)\\",.*?}')
    result = pat.findall(page_source)
    if result:
        promotion = result[0]
    return promotion


def get_favorites(page_source):
    """
    :param page_source: 商品网页源代码
    :return: favorites: 人气
    """
    favorites = ''
    pat = re.compile(r'"apiBeans":"(.*)","idsMod"')
    favorites_url = pat.findall(page_source)
    if not favorites_url:
        return favorites
    api_beans = 'https:' + favorites_url[0]
    icp = api_beans.split(',')[-1]
    api = api_beans + '&callback=json'
    favorites_page_source = get_page_source(api)
    if not favorites_page_source:
        return favorites
    pat = re.compile(r'"{}":(\d+)'.format(icp))
    result = pat.findall(favorites_page_source)
    if result:
        favorites = result[0]
    return favorites


def get_list_price(page_source):
    """
    :param page_source: 商品网页源代码
    :return: list_price: 价格
    """
    list_price = ''
    pat = re.compile(r'"defaultItemPrice":"(\d+.\d+)"')
    result = pat.findall(page_source)
    if result:
        list_price = result[0]        
    return list_price


def get_accumulated_reviews(item_id, use_proxy=False, proxies=None):
    """
    :param item_id: 商品ID
    :param use_proxy: 是否使用代理
    :param proxies: 代理
    :return: accumulated_reviews: 累计评价
    """
    accumulated_reviews = ''
    accumulated_reviews_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=' + item_id
    page_source = get_page_source(accumulated_reviews_url, use_proxy, proxies)
    if not page_source:
        return accumulated_reviews
    pat = re.compile(r'"rateTotal":(\d+)')
    result = pat.findall(page_source)
    if result:
        accumulated_reviews = result[0]
    return accumulated_reviews


def get_tag_page_source(item_id, use_proxy=False, proxies=None):
    tag_url = 'https://rate.tmall.com/listTagClouds.htm?itemId={}&isAll=true'.format(item_id)
    page_source = get_page_source(tag_url, use_proxy, proxies)
    return page_source


def get_tag_count(page_source):
    """
    :param page_source: 标签网页源代码
    :return: tag_count: 标签个数
    """
    tag_count = '0'
    if not page_source:
        return tag_count
    pat = re.compile(r'"tag":"(.*?)"}')
    result = pat.findall(page_source)
    if result:
        tag_count = str(len(set(result)))
    return tag_count


def get_tag(page_source):
    """
    :param page_source: 标签网页源代码
    :return: tag: 标签
    """
    tag = ''
    if not page_source:
        return tag
    pat = re.compile(r'"tag":"(.*?)"}')
    result = pat.findall(page_source)
    if result:
        tag = result
        tag = list_to_string(tag)
    return tag


def get_colors(tree):
    """
    :param tree: 对象
    :return: colors: 颜色
    """
    colors = ''
    xpath_expr = '//li[@title]/a/span'
    result = tree.xpath(xpath_expr)
    if result:
        colors = [_.xpath('text()')[0] for _ in result]
        colors = list_to_string(colors)
    return colors


def get_specs_additional_urls_page_source(page_source, use_proxy=False, proxies=None):
    """
    :param use_proxy: 是否使用代理
    :param proxies: 代理
    :param page_source: 商品网页源代码
    :return: specs: 产品规格说明列表
    """
    specs_additional_urls_page_source = ''
    pat = re.compile(r'"httpsDescUrl":"(.*?)",')
    result = pat.findall(page_source)
    if result:
        _url = 'https:' + result[0]
        specs_additional_urls_page_source = get_page_source(_url, use_proxy, proxies)
    return specs_additional_urls_page_source


def get_specs(page_source):
    """
    :param page_source: 产品规格说明网页和其它相关图片链接源代码
    :return: specs: 产品规格说明列表
    """
    specs = ''
    if not page_source:
        return specs
    pat = re.compile(r'>(.*?)<')
    result = pat.findall(page_source)
    if result:
        specs = list(filter(lambda x: len(x.strip()) != 0, result))
        specs = list_to_string(specs)
    return specs


def get_additional_urls(page_source):
    """
    :param page_source: 产品规格说明网页和其它相关图片链接源代码
    :return: additional_urls: 其它相关图片链接
    """
    additional_urls = ''
    if not page_source:
        return additional_urls
    pat = re.compile(r'src="(.*?)"')
    result = pat.findall(page_source)
    result_ = list(set(result))
    result_.sort(key=result.index)
    if result_:
        additional_urls = result_
        additional_urls = list_to_string(additional_urls)
    return additional_urls


def get_description(page_source):
    """
    :param page_source: 商品网页源代码
    :return: description: 说明
    """
    description = ''
    pat = re.compile(r'<meta name="description" content="(.*?)"/>')
    result = pat.findall(page_source)
    if result:
        description = result[0]
    return description


def get_seller_nickname(page_source):
    """
    :param page_source: 商品网页源代码
    :return: seller_nickname: 昵称
    """
    seller_nickname = ''
    pat = re.compile(r'<a class="slogo-shopname".*><strong>(.*)</strong></a>')
    result = pat.findall(page_source)
    if result:
        seller_nickname = result[0]
    return seller_nickname


def get_seller_region(page_source):
    """
    :param page_source: 商品网页源代码
    :return: seller_region: 发货地区
    """
    seller_region = ''
    pat = re.compile(r'<input type="hidden" name="region" value="(.*?)" />')
    result = pat.findall(page_source)
    if result:
        seller_region = result[0]
    return seller_region


def get_product_skus(page_source):
    """
    :param page_source: 商品网页源代码
    :return: product_skus:
    """
    product_skus = ''
    pat = re.compile(r'"skuId":"(\d+)"')
    result = pat.findall(page_source)
    if result:
        product_skus = list(set(result))
        product_skus.sort()
        product_skus = list_to_string(product_skus)
    return product_skus


def give_me_proxy():
    while True:
        if not producer_queue.empty():
            _ = producer_queue.get()
            proxy = {
                'https': 'https://{}'.format(_),
                'http': 'http://{}'.format(_),
            }
            used = True
            return proxy, used
        # 如果代理全部用完，就用本地IP直接请求
        if not mark_proxy_use_queue.empty():
            proxy = None
            used = False
            return proxy, used


def main_detail(category, category_id, item_id, title, api):
    proxy, used = give_me_proxy()
    if proxy:
        message = proxy.get('https') + ' is used for ' + api
        logger.info(message)

    page_source = get_page_source(api, use_proxy=used, proxies=proxy)
    if not page_source:
        return

    tree = get_tree(page_source)

    colors = get_colors(tree)

    tag_page_source = get_tag_page_source(item_id, use_proxy=used, proxies=proxy)
    accumulated_reviews = get_accumulated_reviews(item_id, use_proxy=used, proxies=proxy)
    monthly_sales_promotion_page = get_monthly_sales_promotion_page_source(item_id, use_proxy=used, proxies=proxy)
    specs_additional_urls_page = get_specs_additional_urls_page_source(page_source, use_proxy=used, proxies=proxy)

    inventory = get_inventory(page_source)
    favorites = get_favorites(page_source)
    list_price = get_list_price(page_source)
    description = get_description(page_source)
    product_skus = get_product_skus(page_source)
    seller_region = get_seller_region(page_source)
    seller_nickname = get_seller_nickname(page_source)

    tag = get_tag(tag_page_source)
    tag_count = get_tag_count(tag_page_source)
    
    promotion = get_promotion(monthly_sales_promotion_page)
    monthly_sales = get_monthly_sales(monthly_sales_promotion_page)
    
    specs = get_specs(specs_additional_urls_page)
    additional_urls = get_additional_urls(specs_additional_urls_page)
    
    data = [category, item_id, title, inventory, monthly_sales, 
            favorites, list_price, promotion, accumulated_reviews, tag_count, 
            tag, colors, specs, title, description, 
            api, seller_nickname, seller_region, additional_urls, product_skus,
            category_id,
            ]
    detail_all.append(data)
    logger.info('crawl {} succeed'.format(api))
    print(data)
    return data


if __name__ == '__main__':
    url = 'https://detail.tmall.com/item.htm?id=528571750194&rn=a1d6b4b5aa65a41e94d4ed23a4aba4a4&abbucket=1'
    main_detail('婴儿（80-100cm）', '1008988062', '567137114877', '无印良品 MUJI 婴儿  法国亚麻水洗短袖连衣裙', url)
