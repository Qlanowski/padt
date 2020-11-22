import requests
import csv
import os
from bs4 import BeautifulSoup
from unicodedata import normalize
from pathlib import Path

csvFileName = "alkohol.csv"
txtFileName = "alkohol.txt"
category = Path(txtFileName).stem

def getData(url):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content.decode('utf-8', 'ignore'), 'html.parser')
    return soup

def parseUrl(url, ind):
    data = getData(url)
    size, package, code = getProductInfo(data)
    images = getProductImages(data)
    brand, product = getProductTitle(data)
    description = getProductDescription(data)
    rate = getProductRating(data)
    extras = {"nutritional" : getNutritional(data), "package": package}

    fields=[ind, code, size, brand, size, category, description, extras, images, "", "", "", "Swiadome zakupy", "", product, url, ""]
    writeRowToCsv(fields)

def getProductInfo(data):
    div = data.find("div", class_="well well-small")
    divContent = div.contents[1].contents
    size, package, code = "", "", ""
    if len(divContent) > 1:
        size = divContent[1]
    if len(divContent) > 3:
        package = divContent[3]
    if len(divContent) > 5:
        code = divContent[5]

    return size, package, code

def getProductImages(data):
    images = []
    thumbnailDivs = data.find_all("div", class_="thumbnail")
    for div in thumbnailDivs:
        for a in div.find_all('a'):
            images.append(a.get('href'))

    for a in data.find_all("a", class_="thumbnail"):
        images.append(a.get('href'))
    
    return images

def getProductTitle(data):
    div = data.find("div", class_="span5")
    brand = div.find("h2").contents[0]
    product = div.find("h3").contents[0]
    return brand, product

def getProductDescription(data):
    div = data.find("div", class_="span5")
    desc = div.find("p").contents[0]
    return desc

def getProductRating(data):
    return data.find("h1", class_="rate-winner").contents[0]

def getNutritional(data):
    div = data.find("div", class_="nutritional")
    nutritional = ""
    if div is None:
        return nutritional

    for nutritionalData in div.find_all('p'):
        nutritional = nutritional + nutritionalData.text + ", "

    return nutritional

def writeRowToCsv(fields):
    isFileExists = os.path.isfile(csvFileName) and os.path.getsize(csvFileName) > 0
    with open(csvFileName, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not isFileExists:
            writer.writerow(",EAN,amount,brand,capacity,category,description,extras,image_url,ingredients,origin,price,seller,storage,title,url,weight".split(','))
        writer.writerow(fields) 

# Using readlines()
file = open(txtFileName, 'r') 
urls = file.readlines() 
for ind, url in enumerate(urls):
    parseUrl(url, ind)
