# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgriscrapperItem(scrapy.Item):
    commodity = scrapy.Field()
    classification = scrapy.Field()
    grade = scrapy.Field()
    sex = scrapy.Field()
    market = scrapy.Field()
    wholesale = scrapy.Field()
    retail = scrapy.Field()
    supply_volume = scrapy.Field()
    county = scrapy.Field()
    date = scrapy.Field()
