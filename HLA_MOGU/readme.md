# 安装环境
```
1.安装Anaconda3


2.安装Python3.5虚拟环境
命令 ---> conda create --name python35 python=3.5
[备用]如果虚拟环境安装出现问题
可以用命令 ---> conda remove --name python35 --all
删除虚拟环境重新执行第2步的安装命令


3.激活虚拟环境
source activate python35


4.安装依赖库
    4.1安装requests
    命令 ---> conda install requests
    
    4.2安装lxml
    命令 ---> conda install lxml
```



# 部署程序
```
1.配置文件config.ini修改, 需要修改的地方:
请用你的目录替换<directory>
    1.1目录的设置
    log_path = /<directory>/HLA_MOGU/logs
    file_system = /<directory>/HLA_MOGU/FileSystem
    file_path_1 = /<directory>/HLA_MOGU/FileSystem/shop_auction_search
    file_path_2 = /<directory>/HLA_MOGU/FileSystem/merchandise_api
    file_path_3 = /<directory>/HLA_MOGU/FileSystem/merchandise_detail
    cookie_path = /<directory>/HLA_MOGU/cookie.txt
    
    1.2邮箱的设置
    sender = xxx@126.com    --->发件人邮箱
    pwd = xxx    --->发件人邮箱客户端授权码, 如果没有开通, 请登录邮箱开通
    receiver = xxx@icloud.com, xxx@163.com, xxx@qq.com    --->收件人列表, 用逗号隔开
    email_host = smtp.126.com    --->SMTP发件服务器地址
    port = 25    --->邮箱端口


2.设置定时
    2.1打开定时
    命令 ---> crontab -e
    
    2.2定时命令
    进入编辑模式输入如下wq保存退出
    比如定时每周一下午6点运行
    命令 ---> 0 18 * * 1 /root/anaconda3/envs/python35/bin/python /<directory>/muji_spider.py
    [备注]muji_spidr是程序的顶层文件, 替换muji_spidr所在的<directory>
    /root/anaconda3/envs/python35/bin/python是安装的python3.5虚拟环境路径   
```
