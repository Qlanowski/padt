# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GroceryScrapperItem(scrapy.Item):
    price = scrapy.Field()
    photo_url = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    ean = scrapy.Field()
    title = scrapy.Field()
    price_before_discount = scrapy.Field()
    price_per_quantity = scrapy.Field()
    category = scrapy.Field()
    packaging = scrapy.Field()
    nutrition = scrapy.Field()
    features = scrapy.Field()
    ingredients = scrapy.Field()
    chemicals = scrapy.Field()
    url = scrapy.Field()
    storage = scrapy.Field()

class CarrefourGroceryScrapperItem(scrapy.Item):
    price = scrapy.Field()
    photo_url = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    storage = scrapy.Field()
    ingredients = scrapy.Field()
    url = scrapy.Field()
    amount = scrapy.Field()
    capacity = scrapy.Field()


class JoinedGroceryScrapperItem(scrapy.Item):
    EAN = scrapy.Field()
    amount = scrapy.Field()
    brand = scrapy.Field()
    capacity = scrapy.Field()
    category = scrapy.Field()
    extras = scrapy.Field()
    image_url = scrapy.Field()
    ingredients = scrapy.Field()
    origin = scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    storage = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    weight = scrapy.Field()
