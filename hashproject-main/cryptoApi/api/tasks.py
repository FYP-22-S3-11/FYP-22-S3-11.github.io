# Scrap data from coinlore.com and save into database 
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from api.serializers import CryptoSerializer, CoinSerializer
from bs4 import BeautifulSoup
from .models import Crypto, Coin
import requests

@shared_task(name = "coin_scraping")
def coin_scraping():
    print(f"Celery is working!! Message is coin scraping")
    headers = {
        'Cookie': 'clogin_session=fmac48uek6s9jkuqniuqjps93h'
    }

    url = "https://www.coinlore.com"
    Coin.objects.all().delete()
    response = requests.request("GET", url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    listingHash = []

    # Find select tag
    select_tag = soup.find("select", attrs={'name': 'algo'})

    # find all option tag inside select tag
    hashList = select_tag.find_all("option")
    for item in hashList:
        if (item['value'] is not None and item['value'] != "0"):
            listingHash.append(item['value'])

    listings = []

    for itemCoins in listingHash:
        final_url = '/'.join([url, 'coins', itemCoins])
        print("final_url", final_url)
        responseHash = requests.request("GET", final_url, headers=headers)

        soup = BeautifulSoup(responseHash.text, "html.parser")

        for item in soup.findAll('tr'):

            name = item.find(
                'small', attrs={'class': 'd-block text-muted coin-name'})
            symbol = item.find(
                'span', attrs={'class': 'coin-ticker'})
            img = item.find('img')

            marketcap = item.find('td', attrs={'class': 'market-cap'})
            price = item.find(
                'div', attrs={'class': 'price_td table-price-class'})
            volume = item.find('a', attrs={'class': 'volume'})
            percent24 = item.find('td', attrs={'class': [
                                  'text-nowrap percent-24h text-right positive_24', 'text-nowrap percent-24h text-right negative_24']})

            if (name is not None):

                listings.append({"name": '' if (name is None) else name.text,
                                "symbol": '' if (symbol is None) else symbol.text,
                                 "img": img['data-src'] if (img is not None and img.has_attr('data-src')) else img['src'] if (img is not None and img.has_attr(
                                     'src')) else "",
                                 "marketcap": '0' if (marketcap is None) else marketcap.text,
                                 "price": '0' if (price is None) else price.text,
                                 "volume": '0' if (volume is None) else volume.text.replace("\n", ""),
                                 "percent": '0' if (percent24 is None) else percent24.text,
                                 "hash": itemCoins})
    # print("listings", listings)

    all_coins = '/'.join([url, 'all_coins'])
    print("final_url", all_coins)

    allResponseHash = requests.request("GET", all_coins, headers=headers)

    allSoup = BeautifulSoup(allResponseHash.text, "html.parser")

    for item in allSoup.findAll('tr'):

            name = item.find(
                'a', attrs={'class': 'm-c-name'})
            symbol = item.find(
                'span', attrs={'class': 'c-symbol d-block d-sm-none'})
            img = item.find('img')

            marketcap = item.find('td', attrs={'class': 'no-wrap market-cap text-right'})
            price = item.find(
                'a', attrs={'class': 'price'})
            volume = item.find('a', attrs={'class': 'volume'})
            percent24 = item.find('td', attrs={'class': [
                                  'no-wrap percent-24h text-right positive_24', 'no-wrap percent-24h text-right negative_24']})

            if (name is not None):

                listings.append({"name": '' if (name is None) else name.text,
                                "symbol": '' if (symbol is None) else symbol.text,
                                 "img": img['data-src'] if (img is not None and img.has_attr('data-src')) else img['src'] if (img is not None and img.has_attr(
                                     'src')) else "",
                                 "marketcap": '0' if (marketcap is None) else marketcap.text,
                                 "price": '0' if (price is None) else price.text,
                                 "volume": '0' if (volume is None) else volume.text.replace("\n", ""),
                                 "percent": '0' if (percent24 is None) else percent24.text,
                                 "hash": ""})
    # print("listings", listings)
    
    crypto_data = isinstance(listings, list)

    serializer = CoinSerializer(data=listings, many=crypto_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
   
 
@shared_task(name = "hash_scraping")
def hash_scraping():
    print(f"Celery is working!! Message is hash scraping")
    headers = {
        'Cookie': 'clogin_session=fmac48uek6s9jkuqniuqjps93h'
    }
    url = "https://www.coinlore.com/"

    response = requests.request("GET", url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    listings = []

    # Find select tag
    select_tag = soup.find("select", attrs={'name': 'algo'})

    # find all option tag inside select tag
    hashList = select_tag.find_all("option")
    for item in hashList:
        if (item['value'] is not None and item['value'] != "0"):
            listings.append({"name": item['value'], "type": "hash"})

    for item in soup.findAll('tr'):
        name = item.find('a', attrs={'class': 'm-c-name coin-symbol'})
        if (name is not None):
            listings.append({"name": name.text, "type": "coin"})
    Crypto.objects.all().delete()
    
    print("hash scraping list", listings)
    

    crypto_data = isinstance(listings, list)

    serializer = CryptoSerializer(data=listings, many=crypto_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
