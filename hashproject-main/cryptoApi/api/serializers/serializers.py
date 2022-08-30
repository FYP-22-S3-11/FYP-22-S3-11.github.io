from rest_framework import serializers 
from api.models import Crypto
 
 
class CryptoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Crypto
        fields = ('id', 'name')