#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test."""

from bs4 import BeautifulSoup

soup = BeautifulSoup(open('email.html'), 'lxml')  # read local html model
i = 0
message = ["first", "second"]
for ul_tag in soup.find_all('ul'):
    ul_tag.clear()  # 移除更新列表中的内容
    new_li_tag = soup.new_tag("li")
    new_li_tag.string = message[i]
    ul_tag.append(new_li_tag)
    i = i + 1
print soup
