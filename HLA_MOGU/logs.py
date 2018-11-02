# -*- coding: utf-8 -*-
import os
import sys
import time
import logging

from utility.util_constant import log_path


def get_today_log():
    today = time.localtime()
    today = time.strftime('%Y-%m-%d', today)
    today_log = today + '.log'
    today_log = os.path.join(log_path, today_log)
    return today_log


# 获取logger实例, 如果参数为空则返回root logger
logger = logging.getLogger()

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)s %(levelname)s: %(message)s')

# 文件日志
file_handler = logging.FileHandler(get_today_log(), encoding='utf-8')
file_handler.setFormatter(formatter)  # 通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器, 可以自定义日志处理器让其输出到其他地方
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别, 默认为WARNING级别, 输出设定级别以上的级别包括本身
logger.setLevel(logging.INFO)
