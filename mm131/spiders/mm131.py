# -*- coding: utf-8 -*-

import scrapy

from ..items import Mm131Item


class Mm131Spider(scrapy.Spider):
    name = 'mm131'
    start_urls = [
        'https://www.mm131.net/xinggan/',
        'https://www.mm131.net/qingchun/',
        'https://www.mm131.net/xiaohua/',
        'https://www.mm131.net/chemo/',
        'https://www.mm131.net/qipao/',
        'https://www.mm131.net/mingxing/',
        ]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "cookie": "Hm_lvt_672e68bf7e214b45f4790840981cdf99=1564544078; UM_distinctid=16c46a17c4494e-0c1df29fb4ff0a-3a75045d-1fa400-16c46a17c452ae; CNZZDATA1277874215=1740849392-1564550394-%7C1564550394; Hm_lpvt_672e68bf7e214b45f4790840981cdf99=1564555786",
    }

    def parse(self, response):
        girls = response.xpath('//dl[@class="list-left public-box"]/dd[not(@class)]')
        for girl in girls:
            imgs_url = girl.xpath('.//a/@href').extract_first()
            yield scrapy.Request(imgs_url, callback=self.content)

        next_page = response.xpath('//dl[@class="list-left public-box"]/dd[@class="page"]/a')[-2]
        next_page_text = next_page.xpath('./text()').extract()[0]
        if next_page_text == "下一页":
            suffix_url = next_page.xpath('./@href').extract()[0]

            # 第一种方法：字符串处理成下一页url
            # lst = response.url.split("/")[:-1]
            # lst.append(suffix_url)
            # next_url = "/".join(lst)
            # print(f"next_url:{next_url}")
            # yield scrapy.Request(next_url, headers=self.headers)

            # 第二种方法：直接response.follow(下一页的后缀)即可
            yield response.follow(suffix_url, headers=self.headers)

    def content(self, response):
        item = Mm131Item()
        item["image_type"] = response.xpath('//div[@class="place"]/a/text()')[1].extract()
        content_xpath = response.xpath('//div[@class="content"]')
        item["title"] = content_xpath.xpath('./h5/text()').extract_first()
        item["image_url"] = content_xpath.xpath('.//div[@class="content-pic"]//img/@src').extract_first()
        item["referer"] = response.url
        yield item

        # 获取下一页按钮的一种写法
        next_urls = content_xpath.xpath('.//div[@class="content-page"]/a[text()="下一页"]/@href').extract()
        if next_urls:
            next_url = next_urls[0]
            yield response.follow(next_url, callback=self.content, headers=self.headers, meta={'item': item})
