# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class AmazonspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = Field()
    name = Field()
    price = Field()
    time = Field()
    author = Field()
    stars = Field()
    comments = Field()

    list_name = Field()
    item_name = Field()
    fen_name = Field()
    list_href = Field()
    item_href = Field()
    fen_href = Field()
    list_num = Field()
    item_num = Field()
    fen_num = Field()

    zongshu = Field()
    yema = Field()
    zishumu = Field()
    url = Field()
    req_url = Field()
    ye = Field()
    



