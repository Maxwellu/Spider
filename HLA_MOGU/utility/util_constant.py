# -*- coding: utf-8 -*-
import os

from utility.util_config import get_config_value

# 无印良品首页API
url = get_config_value('muji_homepage', 'url')
muji_search_url = get_config_value('muji_homepage', 'muji_search_url')

# 保存csv文件系统目录
file_system = get_config_value('filepath_conf', 'file_system')
if not os.path.exists(file_system):
    os.mkdir(file_system)
# 保存shop_auction_search
file_path_1 = get_config_value('filepath_conf', 'file_path_1')
if not os.path.exists(file_path_1):
    os.mkdir(file_path_1)
# 保存merchandise_api
file_path_2 = get_config_value('filepath_conf', 'file_path_2')
if not os.path.exists(file_path_2):
    os.mkdir(file_path_2)
# 保存merchandise_detail
file_path_3 = get_config_value('filepath_conf', 'file_path_3')
if not os.path.exists(file_path_3):
    os.mkdir(file_path_3)

# 记录cookie的文件
cookie_path = get_config_value('cookie_conf', 'cookie_path')

# 线程个数
thread_count = int(get_config_value('thread_conf', 'thread_count'))

# 日志路径
log_path = get_config_value('log_conf', 'log_path')
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 请求响应的超时时间, 单位是秒
request_timeout = int(get_config_value('request_conf', 'request_timeout'))
# 爬取ET代理的时间间隔
proxy_interval = int(get_config_value('proxy_conf', 'proxy_interval'))
# 每一个代理使用的次数
proxy_use_count = int(get_config_value('proxy_conf', 'proxy_use_count'))
# 代理队列的的最大长度
proxy_queue_max = int(get_config_value('proxy_conf', 'proxy_queue_max'))

# 代理
proxy_api = get_config_value('MOGU_Proxy', 'proxy_api')

# 添加白名单接口
add_white_list_api = get_config_value('MOGU_Proxy', 'add_white_list_api')
# 获取白名单接口
get_white_list_api = get_config_value('MOGU_Proxy', 'get_white_list_api')

# 获取查询本地IP的API
local_host_api = get_config_value('local_api', 'local_host_api')

# 文件保留的天数
cycle = int(get_config_value('life_cycle', 'cycle'))

# 邮箱配置
sender_ = get_config_value('email_conf', 'sender')
pwd_ = get_config_value('email_conf', 'pwd')
receiver_ = get_config_value('email_conf', 'receiver')
email_host_ = get_config_value('email_conf', 'email_host')
port_ = int(get_config_value('email_conf', 'port'))

# 没有登录访问的接口异常
error_url = \
      "https://login.taobao.com/member/login.jhtml?style=mini&from=sm&full_redirect=false&redirectURL=https%3a%2f%2f" \
      "muji.tmall.com:443/i/asynSearch.htm/_____tmd_____/punish%3fx5secdata=5e0c8e1365474455070961b803bd560607b52cab" \
      "f5960afff39b64ce58073f78c12c85175e36d0031ebfef2c630355d48aa5e541682b8991707ee43efe6ffc9b9f0450b1b2e052c6ca12a" \
      "a98fef4738f0ef76e349e0b3d859ab74174e72af7d17a79b0125f00b8445f46d6702a7b77610d98e6ac50e5f520014d4d8fc511c89a0d" \
      "ae50f57caef476a00dcb7c27d19198ec37b54036805f2efdac327669d9df49be5b30f6740dfac5f8a7130a495993688f7ce37eea2ad51" \
      "c6d36b6caea56ac55afffbd179e27b17d141a8b6a85e47f925ad8e13001ba8e9cfe8fc0f449703cc70cc2bd052092070786c9d5743ce2" \
      "aa576449645b2b53f99f5b5ae01e7ddd5d16a3b3e7b92e7a104a939356775160b1503cc92d000846649d38cfc8c985642186489019d5f" \
      "fd7cded7305e2667f3d07d246fabac8e27bc6ec8d92390e192c8fd9330a4d6e52d16b36bd3e1c87e3cfc9ea29bc05e9b2940fc42e8db6" \
      "9ecfac5e727799203c629dd111a683472f143c0d1a0cfbad4fe77773d1dc298755ea8d3cef93eb0f6d6cd36fdf475c0174338f6896276" \
      "5b5ecce3c97eb6eaca7d65e6cb80b5994552aad14d878ec4d47bf126542b736cbea4678a109646995834d163f959da4aa3c6fadf3dfc1" \
      "035801bcbac90764df205ec4bbffad9c7a26670a60ff1be35de23572d25cd8a90cbb75ff89c3cc8c2407686ed6515fa24c7ba06df59cc" \
      "255c9c0fa7ff6335ff036bd121fc652ccb6acbfe4dfc841cf2358f977272e5a264fee72ba9f509ac8ad761a2eba22730c45474f41f67e" \
      "ab1712c52bf33d8d3cfc74d397c8c8ea48a2eb663386e8ffde67527e35e29e895dd5559881ed86fa34fa7b%26x5step=100"
