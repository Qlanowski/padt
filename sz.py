# %%
from selenium import webdriver
import time
ALKOHOL = 172
DODATKI_DO_POTRAW_I_CIAST = 200
JEDZENIE_DLA_ZWIERZAT = 209
KAWA_HERBATA_KAKAO = 150
MAKI_PIECZYWO = 66
MIESO = 3
NABIAL = 128
OWOCE = 58
DZIECI = 210
POLPRODUKTY = 107
RYBY = 42
SOL_CUKIER = 120
SLODYCZE = 74
MASLA = 193
WARZYWA_KONSERWY = 51
NAPOJE = 93

# SET PARAMETERS
CATEGORY = ALKOHOL
product_urls_path = "./swiadomezakupy/"+"alkohol2.txt"


# %%
def get_category_url(cat, page=1):
    return f"http://www.swiadomezakupy.pl/search#{str(cat)},,,0,0,0,0,0,0,0,{page}"


def get_page_products_urls(driver):
    return list(map(lambda x: x.get_attribute('href'),
                    driver.find_elements_by_xpath("//li[@class='gridProduct']//a")))


def get_category_products_urls(url):
    url = get_category_url(CATEGORY)
    driver.get(url)
    driver.refresh()
    time.sleep(5)  # czekaj az zniknie kielbasa
    pages = int(driver.find_elements_by_xpath("//li[@data-lp]")[-2].text)
    products = []
    products += get_page_products_urls(driver)
    for i in range(2, pages+1):
        url = get_category_url(CATEGORY, i)
        driver.get(url)
        driver.refresh()
        time.sleep(5)  # czekaj az zniknie kielbasa
        products += get_page_products_urls(driver)
    return list(set(products))


# %%
driver = webdriver.Chrome(
    r".\swiadomezakupy\chromedriver.exe")

url = get_category_url(CATEGORY)
products_urls = get_category_products_urls(url)
driver.quit()

# %%
with open(product_urls_path, 'w+') as filehandle:
    filehandle.write("\n".join(products_urls))