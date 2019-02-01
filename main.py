#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""这是对中国科学技术大学(USTC)研究生招生(研招)网站的监控,如果USTC更新了研招信息，程序将会向指定邮箱发送更新内容."""

# 模块导入
import time
import random
import urllib2
import linecache
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from bs4 import BeautifulSoup

RandomTime = random.randint(0, 600)
time.sleep(RandomTime)

# 读取科大研招网的首页
url = 'http://yz.ustc.edu.cn/'  # 科大研招网的首页
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
Main_Page = response.read()
Main_Page = Main_Page.decode("GBK").encode('UTF-8')
# Main_Page = unicode(Main_Page, 'GBK').encode('UTF-8')
# print(Main_Page)

MainNew = ["新闻动态", 'class="bt01">硕士招生']  # 确定主要搜索的主要信息方向
OldFile = ['OldNews.txt', 'OldMasterEnrollmentMessages.txt']  # 旧信息存放的文件
i = 0  # 初始化索引
count = 0  # 初始化计数器

soup = BeautifulSoup(open('email.html'), 'lxml')  # read local html model
NotUpdate = "Not update"

for ul_tag in soup.find_all('ul'):
    ul_tag.clear()  # 移除更新列表中的内容
    MainNewSite = Main_Page.find(MainNew[i])  # 首先定位信息模块的位置
    # 缩小搜索范围
    TITLE = Main_Page.find(r'title="', MainNewSite)
    BT = Main_Page.find(r'" class=', TITLE)
    New_Msg = Main_Page[TITLE + 7:BT]  # 获取该模块的第一条信息
    Old_New = linecache.getline(OldFile[i], 1).strip('\n')  # 提取该模块以前保存的旧信息
    open(OldFile[i], 'w').write(str(New_Msg))  # 将此次搜索的第一条信息更新文件中
    while New_Msg != Old_New:
        count = count + 1
        new_li_tag = soup.new_tag("li")
        new_li_tag.string = str(New_Msg)
        ul_tag.append(new_li_tag)
        TITLE = Main_Page.find(r'title="', BT)
        BT = Main_Page.find(r'" class=', TITLE)
        New_Msg = Main_Page[TITLE + 7:BT]
        if count > 6:
            count = count - 6
            break
    i = i + 1

# 如果有信息更新则向指定邮箱发送更新信息


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = 'licassisant@outlook.com'
password = '2.71828**'
to_addr = 'liceagle@outlook.com'

msg = MIMEText(str(soup), 'html', 'utf-8')
msg['From'] = _format_addr(u'蜘女 <%s>' % from_addr)
msg['To'] = _format_addr(u'李闯 <%s>' % to_addr)
msg['Subject'] = Header(u'USTC updated the messages', 'utf-8').encode()

time.sleep(RandomTime)

if count:
    try:
        s = smtplib.SMTP()
        s.connect('smtp-mail.outlook.com', 587)
        s.starttls()
        s.login(from_addr, password)
        s.sendmail(from_addr, [to_addr], msg.as_string())
        s.close()
    except smtplib.SMTPException:  # Didn't make an instance.
        pass
    except smtplib.socket.error:
        pass
