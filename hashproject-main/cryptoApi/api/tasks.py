# Scrap data from coinlore.com and save into database 
from celery import shared_task
from cryptoApi.tasks import CustomClsTask
from api.serializers import CryptoSerializer, CoinSerializer
from bs4 import BeautifulSoup
from .models import  Coin
import requests

@shared_task()
def get_list_coin_celery_demo():
    print("demo")
     # checking for the parameters from the URL
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

            name = item.find('a', attrs={'class': 'm-c-name'})
            symbol = item.find(
                'span', attrs={'class': 'c-symbol d-block d-sm-none'})
            img = item.find('img')

            marketcap = item.find('td', attrs={'class': 'market-cap'})
            price = item.find(
                'div', attrs={'class': 'price_td table-price-class'})
            volume = item.find('a', attrs={'class': 'volume'})
            percent24 = item.find('td', attrs={'class': [
                                  'text-nowrap percent-24h text-right positive_24', 'text-right negative_24']})

            if (marketcap is not None):
                listings.append({"name": name.text,
                                 "symbol": symbol.text,
                                 "img": img['data-src'] if (img is not None and img.has_attr('data-src')) else img['src'] if (img is not None and img.has_attr(
                                     'src')) else "",
                                 "marketcap": marketcap.text,
                                 "price": price.text,
                                 "volume": '' if (volume is None) else volume.text.replace("\n", ""),
                                 "percent": '0' if (percent24 is None) else percent24.text,
                                 "hash": itemCoins})
    # print("listings", listings)
    crypto_data = isinstance(listings, list)

    serializer = CoinSerializer(data=listings, many=crypto_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    pass




@shared_task(name = "print_msg_main")
def print_message(message, *args, **kwargs):
    print(f"Celery is working!! Message is {message}")
    
    file1 = open("myfile.txt", "w")
    L = ["This is Delhi \n", "This is Paris \n", "This is London"]
    file1.writelines(L)
    file1.close()