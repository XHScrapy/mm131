# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Mm131Item(scrapy.Item):
    title = scrapy.Field()      # 图片标题
    referer = scrapy.Field()    # 重定向url
    image_url = scrapy.Field()  # 图片真实url
    image_type = scrapy.Field() # 图片分类
