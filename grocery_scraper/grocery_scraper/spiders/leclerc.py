import scrapy
import re
from ..items import GroceryScrapperItem

class LeclercSpider(scrapy.Spider):
    name = "leclerc"
    _base_url = 'https://www.leclerc.rzeszow.pl'
    _category_url = ''
    custom_settings = {
        'ITEM_PIPELINES': {
            'grocery_scraper.pipelines.LeclercScraperPipeline': 300,
        }
    }

    def __init__(self, category='', **kwargs):
        self._category = category
        self.start_urls = [self._base_url]  # py36
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        self._category_url = self.create_category_url(response)
        return scrapy.Request(url=self.create_page_url(0), callback=self.parse_category_pages)

    def parse_category_pages(self, response):
        page = int(response.css('.stronicowanie')[0].css('.nr a::text').getall()[-1])
        for i in range(1, page + 1):
            yield scrapy.Request(url=self.create_page_url(i), callback=self.parse_page)

    def parse_page(self, response):
        absolute_urls =  [self._base_url + url for url in response.css('.inside h2 a::attr(href)').getall()]
        requests = [scrapy.Request(url=url, callback=self.parse_item) for url in absolute_urls]
        for request in requests:
            yield request
    
    def parse_item(self, response):
        item = GroceryScrapperItem()
        item['price'] = response.css('.cena::text').get(default='')
        item['ean'] = response.css('.Ean::text').get(default='')
        item['title'] = response.css('.prod_right h1::text').get(default='')
        item['photo_url'] =  self._base_url + response.css('.thumbnail img::attr(src)').get(default='')
        item['price_before_discount'] = response.css('.cena_taniej::text').get(default='')
        item['price_per_quantity'] = response.css('.price_ilosc::text').get(default='')
        item['category'] = response.css('.breadcrumps span::text').getall()[1:]
        item['packaging'] = self.get_packaging(response)
        item['nutrition'] = self.get_nutrition_table(response)
        item['features'] = self.get_features(response)
        item['ingredients'] = self.get_ingredients(response)
        item['chemicals'] = self.get_chemicals(response)
        item['description'] = self.get_description(response)
        item['url'] = response.url
        item['storage'] = self.get_storage(response)

        return item

    def create_category_url(self, response):
        category_index = [item.strip().lower() for item in response.css('.menu_col .li a::text').getall()].index(self._category)
        category_relative_url =  [item for item in response.css('.menu_col .li a::attr(href)').getall()][category_index]
        category_processed_url = category_relative_url.split(',')[0]
        return category_processed_url

    def create_page_url(self, page): 
        return f'{self._base_url}/{self._category_url},{page}.html'

    def get_description(self, response):
        items = response.css('#brandbank_opis > *').getall()
        textmatch = [item for item in items if item.startswith('<h3>')]
        if len(textmatch) < 2:
            return ''
        textmatch = textmatch[1]
        textmatch = textmatch[4:-5]
        texts = response.css('#brandbank_opis > *::text').getall()
        return ' '.join(texts[1:texts.index(textmatch)])

    def get_storage(self, response):
        storage_header = 'Przechowywanie'
        items = response.css('#brandbank_opis > *').getall()
        headers = [item[4:-5] for item in items if item.startswith('<h3>')]
        if storage_header not in headers:
            return ''
        texts = response.css('#brandbank_opis > *::text').getall()
        storage_texts_index = texts.index(storage_header)
        storage_headers_index = headers.index(storage_header)

        texts_final = []
        if storage_headers_index == len(headers) - 1:
            texts_final = texts[storage_texts_index+1:]
        else:
            other_header = headers[storage_headers_index + 1]
            texts_final = texts[storage_texts_index+1:texts.index(other_header)] 

        return ' '.join(texts_final)

    def get_ingredients(self, response):
        ingredients_base = response.css('.skladniki_left li::text').getall()
        return ingredients_base if len(ingredients_base) > 0 else None

    def get_chemicals(self, response):
        ingredients_chemicals = response.css('.skladniki li::text').getall()
        return ingredients_chemicals if len(ingredients_chemicals) > 0 else None


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