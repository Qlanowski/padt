import scrapy
import re
from ..items import CarrefourGroceryScrapperItem
import json

class CarregourSpider(scrapy.Spider):
    name = 'carrefour'
    _base_url = 'http://carrefour.pl'
    custom_settings = {
        'ITEM_PIPELINES': {
            'grocery_scraper.pipelines.CarrefourScraperPipeline': 300,
        }
    }

    def __init__(self, category='', **kwargs):
        self._category = category
        self.start_urls = [self._base_url]  # py36
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        category_relative_url = self.get_category(response, self._category)
        self._category_url = self.create_category_url(category_relative_url)
        return scrapy.Request(url=self._category_url, callback=self.parse_category)

    def parse_category(self, response):
        page = self.get_page(response)
        for i in range(0, page):
            yield scrapy.Request(url=self.create_page_url(i), callback=self.parse_page)

    def parse_page(self, response):
        json_data = json.loads(response.css('#__NEXT_DATA__::text').get())

        absolute_urls =  [self._base_url + '/' + item['url'] for item in json_data['props']['initialState']['products']['data']['content']]
        requests = [scrapy.Request(url=url, callback=self.parse_item) for url in absolute_urls]
        for request in requests:
            yield request
    
    def parse_item(self, response):
        item = CarrefourGroceryScrapperItem()
        item['title'] = response.css('h1.MuiTypography-root.MuiTypography-h1::text').get(default='')
        item['description'] = self.get_description(response)
        item['price'] = response.css('div.MuiTypography-root.MuiTypography-h1::text').get(default='')
        item['photo_url'] = response.css('.react-swipeable-view-container img::attr(src)').get(default='')
        item['category'] = response.css('.MuiBreadcrumbs-ol .MuiButton-label::text').getall()[1:]
        item['amount'] = response.css('.MuiTypography-colorTextSecondary b::text').get(default='')
        item['url'] = response.url
        item['storage'], item['ingredients'] = self.parse_json(response)

        return item


    def get_page(self, response):
        page_element = response.css('div.MuiOutlinedInput-root ~  p.MuiTypography-root.MuiTypography-body1::text').getall()[1]
        return int(''.join(filter(str.isdigit, page_element)))

    def get_category(self, response, category_name):
        json_to_parse = json.loads(response.css('#__NEXT_DATA__::text').get())
        categories_tree_root =  json_to_parse['props']['initialState']['categories']['data']
        return self.get_category_from_tree(categories_tree_root, category_name)

    def get_category_from_tree(self, root, category_name):
        if 'children' not in root:
            return None
        for child in root['children']:
            if child['name'].lower() == category_name.lower():
                return child['url']
            child_result = self.get_category_from_tree(child, category_name)
            if child_result != None:
                return child_result
        return None


    def get_description(self, response):
        header =  response.css('.MuiTab-wrapper span::text').get(default = '')
        return (None if header != 'Opis' else 
                response.css('.react-swipeable-view-container > div > div::text').get(default=''))

    def create_category_url(self, category_relative_url):
        return f'{self._base_url}/{category_relative_url}'

    def create_page_url(self, page): 
        return f'{self._category_url}?page={page}'

    def parse_json(self, response):
        json_to_parse = json.loads(response.css('#__NEXT_DATA__::text').get())
        description_attributes =  json_to_parse['props']['initialState']['product']['data']['descriptionAttributeSets'][0]['descriptionAttributes']

        storage = [item['value'] for item in description_attributes if item['name'] == 'Przechowywanie']
        storage = storage[0] if len(storage) > 0 else None
        ingredients = [item['value'] for item in description_attributes if item['name'] == 'Składniki']
        ingredients = ingredients[0] if len(ingredients) > 0 else None
        return storage, ingredients

