from django_cron import CronJobBase, Schedule

from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .models import Crypto, Coin
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from api.serializers import CryptoSerializer, CoinSerializer
import re
from rest_framework.permissions import AllowAny


class MyCronJob(CronJobBase):
    permission_classes = [AllowAny]

    RUN_EVERY_MINS = 1 # every 5 minutes
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'api.my_cron_job'    # a unique code

    def do(self):
        headers = {
        'Cookie': 'clogin_session=fmac48uek6s9jkuqniuqjps93h'
        }
        url = "https://www.coinlore.com/"

        response = requests.request("GET", url, headers=headers)
        if (response is not None):
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

            crypto_data = isinstance(listings, list)

            serializer = CryptoSerializer(data=listings, many=crypto_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        pass    
