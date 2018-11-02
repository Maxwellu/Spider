# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from logs import logger
from utility.util_constant import sender_, pwd_, receiver_, email_host_, port_


class SendMailBase(object):
    def __init__(self, title, content, sender=sender_, pwd=pwd_,
                 email_host=email_host_, port=port_, receiver=None, file=None):
        self.sender = sender  # 发件人邮箱
        self.pwd = pwd  # 发件人邮箱的客户端授权码
        self.receiver = receiver  # 接收人邮箱
        self.title = title  # 邮件标题
        self.content = content  # 邮件内容
        self.file = file  # 邮件附件
        self.email_host = email_host  # 邮箱协议
        self.port = port  # 邮箱端口号
        self.smtp = smtplib.SMTP(self.email_host, port=self.port)  # 发送邮件服务器的对象

    def send_mail(self):
        msg = MIMEMultipart()  # 发送内容的对象
        # 处理附件的
        if self.file:
            att = MIMEText(open(self.file).read())
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % self.file
            msg.attach(att)
        msg.attach(MIMEText(self.content))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.sender  # 发送者账号
        msg['To'] = self.receiver  # 接收者账号
        try:
            self.smtp.login(self.sender, self.pwd)
            self.smtp.sendmail(self.sender, self.receiver, msg.as_string())
        except Exception as e:
            logger.error(e)
        else:
            logger.info('send email to {} succeed'.format(self.receiver))

    def __del__(self):
        self.smtp.quit()


class SendMail(object):
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def send_mail(self):
        rec_list = receiver_.split(',')
        rec_list = [_.strip() for _ in rec_list]
        for rec in rec_list:
            obj = SendMailBase(self.title, self.content, receiver=rec)
            obj.send_mail()


if __name__ == '__main__':
    m = SendMail(
        title='开会事宜', content='请所有同事中午到会议室开会',
    )
    m.send_mail()
