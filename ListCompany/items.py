# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListcompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    contact_person = scrapy.Field()
    job_title = scrapy.Field()
    tel_link = scrapy.Field()
    pass
