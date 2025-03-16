from rest_framework import serializers
from .models import Brand, CarModel

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'average_price', 'brand']
        read_only_fields = ['id', 'brand']

class BrandSerializer(serializers.ModelSerializer):
    average_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'average_price']
    
    def get_average_price(self, obj):
        return obj.average_price()
