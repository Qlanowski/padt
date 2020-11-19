# -*- coding: utf-8 -*-
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


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

class GroceryScraperPipeline(object):
    def process_item(self, item, spider):
        item['price'] = text_to_number(item['price'])
        item['ean'] = text_to_ean(item['ean'])
        item['price_before_discount'] = text_to_number(item['price_before_discount'])
        item['price_per_quantity'] = text_to_number(item['price_per_quantity'])
        item['nutrition'] = parse_nutrition(item['nutrition'])

        return item
