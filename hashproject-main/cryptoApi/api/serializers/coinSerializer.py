from rest_framework import serializers 
from api.models import Coin
 
 
class CoinSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Coin
        fields = ('id', 'name', 'hash', 'symbol', 'marketcap', 'price', 'volume', 'percent', 'img', 'last_update_date')