import scrapy
import re
from ..items import GroceryScrapperItem

class LeclercSpider(scrapy.Spider):
    name = "leclerc"
    _base_url = 'https://www.leclerc.rzeszow.pl'
    _categories_dict = {
        'napoje': 'napoje-katalog-10',
        'chemia': 'chemia-katalog-14'
    }
    
    def __init__(self, category='', **kwargs):
        self._category = category
        self.start_urls = [self.create_page_url(category, 1)]  # py36

        super().__init__(**kwargs)  # python3


    def parse(self, response):
        page = int(response.css('.stronicowanie')[0].css('.nr a::text').getall()[-1])
        for i in range(1, page + 1):
            yield scrapy.Request(url=self.create_page_url(self._category, i), callback=self.parse_page)

    def parse_page(self, response):
        relative_urls =  [self._base_url + url for url in response.css('.inside h2 a::attr(href)').getall()]
        requests = [scrapy.Request(url=url, callback=self.parse_item) for url in relative_urls]
        for request in requests:
            yield request
    
    def parse_item(self, response):
        item = GroceryScrapperItem()
        item['price'] = response.css('.cena::text').get(default='')
        item['ean'] = response.css('.Ean::text').get(default='')
        item['title'] = response.css('.prod_right h1::text').get(default='')
        item['photo_url'] = response.css('.thumbnail img::attr(src)').get(default='')
        item['price_before_discount'] = response.css('.cena_taniej::text').get(default='')
        item['price_per_quantity'] = response.css('.price_ilosc::text').get(default='')
        item['category'] = response.css('.breadcrumps span::text').getall()[-1]
        item['packaging'] = self.get_packaging(response)
        item['nutrition'] = self.get_nutrition_table(response)
        item['features'] = self.get_features(response)
        item['ingredients'] = self.get_ingredients(response)

        return item



    def create_page_url(self, category, page): 
        return f'{self._base_url}/{self._categories_dict[category]},{page}.html'

    def get_ingredients(self, response):
        ingredients_chemicals = response.css('.skladniki li::text').getall()
        ingredients_base = response.css('.skladniki_left li::text').getall()
        ingredients = ingredients_base + ingredients_chemicals
        return ingredients if len(ingredients) > 0 else None


    def get_features(self, response):
        features = response.css('div.cechy li::text').getall()
        return features if len(features) > 0 else None

    def get_packaging(self, response):
        packaging_dict = {}
        for (name, value) in zip(
            response.css('.dane td::text').getall(),
            response.css('.dane td > *::text').getall()
        ):
            packaging_dict[name] = value
        return packaging_dict

    def get_nutrition_table(self, response):
        names = response.css('.wartosci_odzywcze tr td:not([align="center"])::text').getall()
        
        if len(names) == 0:
            return None
        values = response.css('.wartosci_odzywcze tr td[align="center"]:not([class="nag blue"])::text').getall()
        names = names[:len(values)]

        nutrition_dict = {}

        for (name, value) in zip (names, values):
            nutrition_dict[name] = value
        return nutrition_dict