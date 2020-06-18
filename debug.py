# -*- coding:utf-8 -*-
'''
@Description: scrapy debug
@Author: lamborghini1993
@Date: 2019-07-30 17:34:28
@UpdateDate: 2019-08-01 09:52:52
'''

import os
import sys

from scrapy.cmdline import execute

dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
execute(["scrapy", "crawl", "mm131"])
