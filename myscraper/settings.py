# -*- coding: utf-8 -*-

BOT_NAME = 'myscraper'

SPIDER_MODULES = ['myscraper.spiders']
NEWSPIDER_MODULE = 'myscraper.spiders'
# DUPEFILTER_DEBUG = False
DUPEFILTER_CLASS =  'scrapy.dupefilter.BaseDupeFilter'