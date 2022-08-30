from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .models import Crypto
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from api.serializers import CryptoSerializer
import re
regex = re.compile(".*?\((.*?)\)")

@api_view(['GET'])
def view_list(request):
    
    # checking for the parameters from the URL
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    payload={}
    headers = {
    'X-CMC_PRO_API_KEY': '7e49e5ac-b3e2-471f-8e6a-2fdeec271197'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return Response(json.loads(response.text))

@api_view(['GET'])
def view_detail(request, id):
    url = "https://www.blockchain.com/explorer/assets"
    final_url = '/'.join([url,id ])
    
    payload={}
    headers = {}

    response = requests.request("GET", final_url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, "html.parser")
   
    listings = []

    for item in soup.findAll('div', {'class':'sc-b69cedd4-0 jFnyqW'}):
       
        key = item.find('div', attrs={'class': 'sc-b69cedd4-1 ekGMji'})
        value = item.find('div', attrs={'class': 'sc-b69cedd4-2 gCEoXO'})
        if(value is not None):
            listings.append({"key": key.text, "value": value.text})


    return Response({"code": 200,"status": "ok", "data": listings})

@api_view(['GET', 'POST', 'DELETE'])
def view_hash_list(request):
    
    if request.method == 'GET':
        cryptos = Crypto.objects.all()
        cryptos_serializer = CryptoSerializer(cryptos, many=True)
        return Response({"data": cryptos_serializer.data})

    elif request.method == 'POST':
        # crypto_data = JSONParser().parse(request)
        data = request.data
        crypto_data = isinstance(data, list)

        serializer = CryptoSerializer(data=data, many=crypto_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
        )

    elif request.method == 'DELETE':
        count = Crypto.objects.all().delete()
        return Response({'message': '{} Cryptos were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def view_coin_list(request, id):
    # checking for the parameters from the URL
    url = "https://www.coinlore.com/coins"
    final_url = '/'.join([url,id ])
    print(final_url)
    headers = {
    'Cookie': 'clogin_session=fmac48uek6s9jkuqniuqjps93h'
    }

    response = requests.request("GET", final_url, headers=headers)
   
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []

    for item in soup.findAll('tr'):
       
        name = item.find('a', attrs={'class': 'm-c-name'})
        symbol = item.find('span', attrs={'class': 'c-symbol d-block d-sm-none'})
        img = item.find('img')
        
        marketcap = item.find('td', attrs={'class': 'market-cap'})
        price = item.find('div', attrs={'class': 'price_td table-price-class'})
        volume = item.find('a', attrs={'class': 'volume'})
        percent24 = item.find('td', attrs={'class': ['text-nowrap percent-24h text-right positive_24', 'text-right negative_24']})

        if(marketcap is not None):
            listings.append({"name": name.text, "symbol": symbol.text , "img": img['data-src'] if(img is not None and img.has_attr('data-src')) else img['src'] if(img is not None and img.has_attr('src')) else "", "market-cap": marketcap.text, "price": price.text, "volume": '' if (volume is None)  else volume.text.replace("\n", ""), "percent24": '' if (percent24 is None)  else percent24.text ,  "algo": id })
    
    return Response({"code": 200,"status": "ok", "data": listings})

@api_view(['GET'])
def view_algo_list(request):
    # checking for the parameters from the URL
    url = "https://www.coinlore.com/"

    headers = {
    'Cookie': 'clogin_session=fmac48uek6s9jkuqniuqjps93h'
    }

    response = requests.request("GET", url, headers=headers)
   
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []

    # Find select tag
    select_tag = soup.find("select" , attrs={'name': 'algo'})

    # find all option tag inside select tag
    hashList = select_tag.find_all("option")
    for item in hashList:
        if(item['value'] is not None and item['value'] != "0"):
            listings.append({"name": item['value'], "type": "hash"})

    for item in soup.findAll('tr'):
        name = item.find('a', attrs={'class': 'm-c-name coin-symbol'})
        if(name is not None):
            listings.append({"name": name.text, "type": "coin"})



    return Response({"code": 200,"status": "ok", "data": listings})

@api_view(['GET'])
def view_coin_detail(request, type, id):
    print(type, id)
    coinUrl = "https://www.coinlore.com/coin"
    headers = {
        'Cookie': 'clogin_session=fmac48uek6s9jkuqniuqjps93h'
        }
      
    if(type == "hash"):
        url = "https://www.coinlore.com/coins"
        final_url = '/'.join([url,id ])
        response = requests.request("GET", final_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        name = soup.findAll('tr')[1].find('a', attrs={'class': 'm-c-name'}).text
    else:
        name = id

    final_url_coin = '/'.join([coinUrl,name ])
    print(name, final_url_coin)
    response = requests.request("GET", final_url_coin, headers=headers)
    coin_soup_detail = BeautifulSoup(response.text, "html.parser")

    coind_d = coin_soup_detail.find('table', attrs={'id': 'coin-d'})
    
    coniDetail = {}
    for item in coind_d.findAll('tr'):
        if(item.find(text='Algorithm')):
            coniDetail["algo"] = item.find('span', attrs={'class': 'badge badge-pill badge-info'}).text
            print(item)
        if(item.find(text='Ticker Symbol')):
            coniDetail["symbol"] = item.find('td').text

    coniDetail["name"] = re.sub("\(.*?\)|\[.*?\]","", coin_soup_detail.find('h2', attrs={'class': 'coin-title m-t-10 cl-coin__name'}).text)

    coniDetail["marketcap"] = coin_soup_detail.find('span', attrs={'id': 'hmcap'}).text if(coin_soup_detail.find('span', attrs={'id': 'hmcap'})) else ""

    coniDetail["price"] = coin_soup_detail.find('span', attrs={'id': 'hprice'}).text if(coin_soup_detail.find('span', attrs={'id': 'hprice'})) else ""
    
    coniDetail["volume"] = coin_soup_detail.find('span', attrs={'id': 'hvol'}).text if(coin_soup_detail.find('span', attrs={'id': 'hvol'})) else ""
    
    coniDetail["percent"] = coin_soup_detail.find('span', attrs={'class': 'price-percent'}).text[coin_soup_detail.find('span', attrs={'class': 'price-percent'}).text.find("(")+1:coin_soup_detail.find('span', attrs={'class': 'price-percent'}).text.find(")")] 
    
    coniDetail["img"] = 'https://www.coinlore.com'+coin_soup_detail.find('div', attrs={'class': 'card coin_left'}).find('picture').find('img')['src'] if(coin_soup_detail.find('div', attrs={'class': 'card coin_left'}).find('picture').find('img') is not None and coin_soup_detail.find('div', attrs={'class': 'card coin_left'}).find('picture').find('img').has_attr('src')) else ""

    print("coniDetail", coniDetail)
    
    return Response({"code": 200,"status": "ok", "data": coniDetail})

