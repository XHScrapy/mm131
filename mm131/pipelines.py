# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re

from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class Mm131Pipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        """下载图片时加入referer请求头"""
        image_url = item['image_url']
        headers = {'referer': item['referer']}
        # 这里把item传过去，因为后面需要用item里面的书名和章节作为文件名
        yield Request(image_url, meta={'item': item}, headers=headers)

    def file_path(self, request, response=None, info=None):
        """修改文件的命名和路径"""
        item = request.meta['item']
        title = item['title']
        fold_name = re.sub(r'[？\\*|“<>:/()0123456789]', '', title)
        image_suf = request.url.split('.')[-1]
        file_name = title + "." + image_suf
        filename = './{}/{}/{}'.format(item['image_type'], fold_name, file_name)
        return filename

    def item_completed(self, results, item, info):
        """获取图片的下载结果, 控制台查看"""
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
