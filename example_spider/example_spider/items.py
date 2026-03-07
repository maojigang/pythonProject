# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleSpiderItem(scrapy.Item):
    title = scrapy.Field()  # 电影名
    score = scrapy.Field()  # 评分
    intro = scrapy.Field()  # 简介
