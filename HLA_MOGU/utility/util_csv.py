# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import datetime

from utility.util_send_email import SendMail


def read_from_csv(file_path):
    """
    读取当天的CSV
    :param file_path: 文件路径
    :return: data
    """
    data = []
    files = os.listdir(file_path)
    today = time.localtime()
    today = time.strftime('%Y-%m-%d', today)
    for _ in files:
        if _.startswith(today):
            file = os.path.join(file_path, _)
            with open(file, 'r', encoding='utf8') as f:
                reader = csv.reader(f)
                for line in reader:
                    data.append(line)
            break
    return data


def write_to_csv(data, file_path):
    """
    中间过渡文件保存到CSV
    :param data: [[], [], []...]
    :param file_path: 文件路径
    :return: None
    """
    today = time.localtime()
    today = time.strftime('%Y-%m-%d', today)
    file_name = today + '.csv'
    file = os.path.join(file_path, file_name)
    with open(file, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        for _ in data:
            writer.writerow(_)


def write_title(file_path):
    """
    在第一行添加字段
    :param file_path: 目录
    :return:
    """
    today = time.localtime()
    today = time.strftime('%Y-%m-%d', today)
    file_name = today + '.csv'
    file = os.path.join(file_path, file_name)
    if os.path.exists(file):
        return
    with open(file, 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        title = ['Time', 'Category', 'Tmall.Id', 'title', 'Inventory', 'MonthlySales', 'Favorites',
                 'ListPrice', 'Promotion', 'AccumulatedReviews', 'TagCount', 'Tags',
                 'Colors', 'Specs', 'Keywords', 'Description', 'ProductURL', 'SellerNickname',
                 'SellerRegion', 'AdditionalURLs', 'ProductSKUs', 'Category.Id']
        writer.writerow(title)


def write_detail_info_to_csv(data, file_path):
    """
    把商品详细信息保存至CSV
    :param data: [[], [], []...]
    :param file_path: 文件路径
    :return: None
    """
    today = time.localtime()
    today = time.strftime('%Y-%m-%d', today)
    file_name = today + '.csv'
    file = os.path.join(file_path, file_name)
    with open(file, 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        for _ in data:
            writer.writerow(_)


def add_time(data):
    """
    在第一列添加时间
    :param data: [[], [], []...]
    :return: [[], [], []...]
    """
    current_time = time.localtime()
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    [_.insert(0, current_time) for _ in data]
    return data


def delete_csv_and_log(file_path, before_days=7):
    """

    :param file_path: 文件路径
    :param before_days: 负数表示不删除,
                        0代表一天也不要,
                        1代表只保留今天的,
                        2代表保留今天和昨天,
                        以此类推...,
                        默认是保留7天
    :return: None
    """
    if before_days < 0:
        return
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=before_days)
    point = today - delta
    files = os.listdir(file_path)
    for file in files:
        if 'DS_Store' in file:
            continue
        file_name = file.split('.')[0]  # 2018-09-28
        file_name_date = datetime.datetime.strptime(file_name, '%Y-%m-%d')
        if file_name_date < point:
            _ = os.path.join(file_path, file)
            os.remove(_)


def delete_barbarism_csv(file_path):
    """
    删除不符合规范的csv文件
    如 2018-10-09-copy.csv不符合
    只保留2018-10-09.csv这种
    :param file_path: 目录
    :return: None
    """
    files = os.listdir(file_path)
    pat = re.compile('\d{4}-\d{2}-\d{2}.csv')
    for file in files:
        result = pat.match(file)
        if not result:
            os.remove(os.path.join(file_path, file))


def check_api_changed(data):
    """
    检查 monthly_sales, accumulated_reviews, tag, specs_additional_urls,
    其索引分别是 5, 9, 11, 13
    :param data: [[], [], []...]
    :return: None
    """
    data_length = len(data)
    none_monthly_sales_count = 0
    none_accumulated_reviews_count = 0
    none_tag_count = 0
    none_specs_additional_urls_count = 0
    for _ in data:
        monthly_sales = _[5]
        accumulated_reviews = _[9]
        tag = _[11]
        specs_additional_urls = _[13]
        if not monthly_sales:
            none_monthly_sales_count += 1
        if not accumulated_reviews:
            none_accumulated_reviews_count += 1
        if not tag:
            none_tag_count += 1
        if not specs_additional_urls:
            none_specs_additional_urls_count += 1
    content = ''
    if none_monthly_sales_count == data_length:
        content_1 = '月销量的API可能发生变动，请手动检查：https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?' \
                    'data=%7B%22itemNumId%22%3A%22563976002360%22%7D 是否有效'
        content += content_1
    if none_accumulated_reviews_count == data_length:
        content_2 = '累计评价API可能发生变动，请手动检查：https://dsr-rate.tmall.com/list_dsr_info.htm?' \
                    'itemId=563976002360 是否有效'
        content += content_2
    if none_tag_count == data_length:
        content_3 = '标签API可能发生变动，请手动检查：https://rate.tmall.com/listTagClouds.htm?' \
                    'itemId=563976002360&isAll=true 是否有效'
        content += content_3
    if none_specs_additional_urls_count == data_length:
        content_4 = '商品说明API可能发生变动，请手动检查：httpsDescUrl后面的API是否有效'
        content += content_4
    if content:
        title = '警告'
        obj = SendMail(title, content)
        obj.send_mail()


if __name__ == '__main__':
    pass
