Swiadome zakupy:
 - pip install selenium
 - do folderu swiadome zakupy pobrac driver chrome - plik exe. Sprawdzić jaką masz wersje chroma (pewnie 86) pobrać zipa ze strony: https://sites.google.com/a/chromium.org/chromedriver/downloads
 - wybrac kategorie i ścieżke gdzie ma zapisać produkty.

Leclerc:
- pip install scrapy
- uruchamia sie poprzez wejscie do folderu grocery_scraper i wklepanie do konsoli 
- scrapy crawl <strona>  -a category=<kategoria>
- dostępne opcje <strona>: carrefour oraz leclerc
- jeżeli nazwa kategorii składa się z więcej niż jednego słowa, należy zamknąć ją w cudzysłowach (")
- jak chce sie output do jsona albo csv to opcja dodatkowa -o plik.json/csv 