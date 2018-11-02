# -*- coding: utf-8 -*-
import time
import threading
from queue import Queue
from datetime import datetime
from multiprocessing import Process

from logs import logger
from product_api import main_product
from merchandise_api import repeat_login
from merchandise_detail import main_detail, detail_all
from merchandise_api import main_merchandise_url
from utility.util_constant import cycle, thread_count
from utility.util_constant import log_path, file_path_1, file_path_2, file_path_3
from utility.util_csv import delete_csv_and_log, delete_barbarism_csv, check_api_changed
from utility.util_proxy import proxy_main, charge_white_list, empty_queue, producer_queue
from utility.util_csv import add_time, read_from_csv, write_title, write_detail_info_to_csv

# 待爬取的商品队列
url_queue = Queue()
# 公用的线程锁
mutex = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, category, category_id, item_id, title, api):
        super(MyThread, self).__init__()
        self.category = category
        self.category_id = category_id
        self.item_id = item_id
        self.title = title
        self.api = api

    def run(self):
        global mutex
        data = main_detail(self.category, self.category_id, self.item_id, self.title, self.api)
        if mutex.acquire():
            if not data:
                logger.info('[{}]这个产品下ID为[{}]的商品下载失败，该商品API是：{}，重新放入商品队列等待爬取！'.
                            format(self.category, self.item_id, self.api))
                logger.info('')
                url_queue.put([self.category, self.category_id, self.item_id, self.title, self.api])
            mutex.release()


def main():
    start_time = datetime.now()

    # 确认cookie正常
    # repeat_login()

    # 删除不合规范的csv
    # delete_barbarism_csv(file_path_1)
    # delete_barbarism_csv(file_path_2)
    # delete_barbarism_csv(file_path_3)

    # 将IP添加到白名单
    # charge_white_list()

    # 第一步, 爬取所有产品
    # main_product()
    # logger.info('main_product finished, please wait 30 seconds!')

    # time.sleep(30)

    # 第二步, 爬取商品URL
    # main_merchandise_url()
    all_data = read_from_csv(file_path_2)
    for _ in all_data:
        url_queue.put(_)
    all_data.clear()

    # 开子进程爬取代理
    proxy_process = Process(target=proxy_main)
    proxy_process.start()

    time.sleep(5)

    while not url_queue.empty():
        thread_list = []
        if url_queue.qsize() >= thread_count:
            for i in range(thread_count):
                data = url_queue.get()
                thread_list.append(MyThread(data[0], data[1], data[2], data[3], data[4]))
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()
            logger.info('商品队列里还剩{}个商品'.format(url_queue.qsize()))
        else:
            for i in range(url_queue.qsize()):
                data = url_queue.get()
                thread_list.append(MyThread(data[0], data[1], data[2], data[3], data[4]))
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()
            logger.info('商品队列里还剩{}个商品'.format(url_queue.qsize()))

    logger.info('商品队列已经全部爬取完成')

    # 商品全部爬取完后, 结束请求代理的进程
    if proxy_process.is_alive():
        proxy_process.terminate()

    # 在第一列加入爬取时间
    new_detail_all = add_time(detail_all)

    # 添加字段
    write_title(file_path_3)

    # 第四步, 把商品详情信息写入CSV文件
    write_detail_info_to_csv(new_detail_all, file_path_3)

    # 检查相关的API是否变动
    check_api_changed(new_detail_all)

    # 清空缓存
    detail_all.clear()
    new_detail_all.clear()

    # 清空队列
    empty_queue(producer_queue)

    # 删除FileSystem里面CSV文件, 只保留近7天的
    delete_csv_and_log(file_path=file_path_1, before_days=cycle)
    delete_csv_and_log(file_path=file_path_2, before_days=cycle)
    delete_csv_and_log(file_path=file_path_3, before_days=cycle)

    # 删除log文件, 只保留近7天的
    delete_csv_and_log(file_path=log_path, before_days=cycle)

    end_time = datetime.now()
    cost_time = (end_time - start_time).seconds / 60.0
    logger.info('本次下载共花费{:.2f}分钟'.format(cost_time))


if __name__ == "__main__":
    main()
