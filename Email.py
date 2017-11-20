#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This email model."""


from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 读取
emailFile = 'email.html'
emailContent = open(emailFile, 'r').read()


from_addr = 'licassisant@outlook.com'
password = '2.71828li'
to_addr = 'liceagle@outlook.com'

msg = MIMEText(emailContent, 'html', 'utf-8')
msg['From'] = _format_addr(u'蜘女 <%s>' % from_addr)
msg['To'] = _format_addr(u'李闯 <%s>' % to_addr)
msg['Subject'] = Header(u'USTC updated the messages', 'utf-8').encode()

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
