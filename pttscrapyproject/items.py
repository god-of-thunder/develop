# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PttscrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    title_name = scrapy.Field()
    published_time = scrapy.Field()
    category_db = scrapy.Field()
    content_text = scrapy.Field()
    canonical_url = scrapy.Field()
    created_time = scrapy.Field()
    update_time = scrapy.Field()
    comment_id = scrapy.Field()
    comment_text = scrapy.Field()
    comment_time = scrapy.Field()
    pass
