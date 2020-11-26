# -*- coding: utf-8 -*-
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .items import JoinedGroceryScrapperItem

def text_to_number(price):
    price = price.replace(',', '.')
    match = re.search(r'\d+(\.\d+)?', price)
    return float(match.group(0)) if match is not None else None

def text_to_ean(ean):
    match = re.search(r'\d+', ean)
    return match.group(0) if match is not None else None

def parse_nutrition(nutrition):
    if nutrition is None:
        return None
    
    res = {}

    for key in nutrition:
        new_key = key.strip()
        new_key = re.sub(r'[*%]', '', new_key)
        res[new_key] = nutrition[key]
    return res

class LeclercScraperPipeline(object):
    def process_item(self, item, spider):
        item['price'] = text_to_number(item['price'])
        item['ean'] = text_to_ean(item['ean'])
        item['price_before_discount'] = text_to_number(item['price_before_discount'])
        item['price_per_quantity'] = text_to_number(item['price_per_quantity'])
        item['nutrition'] = parse_nutrition(item['nutrition'])

        return self.create_joined_item(item)

    def create_joined_item(self, item):
        new_item = JoinedGroceryScrapperItem()

        new_item['EAN'] = item['ean']
        new_item['price'] = item['price']
        new_item['image_url'] = item['photo_url']
        new_item['category'] = ' > '.join(item['category'])
        new_item['description'] = item['description']
        new_item['title'] = item['title']
        new_item['amount'] = item['packaging']['Waga netto:'] if 'Waga netto:' in item['packaging'] else None
        new_item['capacity'] = item['packaging']['Rozmiar opakowania:'] if 'Rozmiar opakowania:' in item['packaging'] else None
        new_item['brand'] = item['packaging']['Producent:'] if 'Producent:' in item['packaging'] else None
        new_item['origin'] = item['packaging']['Kraj pochodzenia:'] if 'Kraj pochodzenia:' in item['packaging'] else None
        new_item['seller'] = 'Leclerc Rzeszów'
        new_item['weight'] = 'Waga netto ' + item['packaging']['Waga netto:'] if 'Waga netto:' in item['packaging'] else None
        new_item['ingredients'] = '\n'.join(item['ingredients']) if item['ingredients'] is not None else None
        new_item['extras'] = '\n'.join(item['chemicals']) if item['chemicals'] is not None  else None
        new_item['url'] = item['url']
        new_item['storage'] = item['storage']

        return new_item

class CarrefourScraperPipeline(object):
    def process_item(self, item, spider):
        item['price'] = text_to_number(item['price'])

        return self.create_joined_item(item)

    def create_joined_item(self, item):
        new_item = JoinedGroceryScrapperItem()

        new_item['price'] = item['price']
        new_item['image_url'] = item['photo_url']
        new_item['category'] = ' > '.join(item['category'])
        new_item['description'] = item['description']
        new_item['title'] = item['title']
        new_item['amount'] = item['amount']       
        new_item['ingredients'] = item['ingredients']
        new_item['url'] = item['url']
        new_item['storage'] = item['storage']
        new_item['seller'] = 'Carrefour'

        return new_item