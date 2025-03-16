from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import Brand, CarModel
from .serializers import BrandSerializer, CarModelSerializer

# GET /brands and POST /brands/
class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def perform_create(self, serializer):
        name = self.request.data.get('name')
        if Brand.objects.filter(name__iexact=name).exists():
            raise ValidationError("The brand name is already in use")
        serializer.save()

# GET and POST /brands/<brand_id>/models/
class BrandModelsListCreateView(generics.ListCreateAPIView):
    serializer_class = CarModelSerializer

    def get_queryset(self):
        brand_id = self.kwargs.get('brand_id')
        # Ensure the brand exists
        get_object_or_404(Brand, id=brand_id)
        return CarModel.objects.filter(brand_id=brand_id)

    def perform_create(self, serializer):
        brand_id = self.kwargs.get('brand_id')
        brand = get_object_or_404(Brand, id=brand_id)
        name = self.request.data.get('name')
        if CarModel.objects.filter(name__iexact=name, brand=brand).exists():
            raise ValidationError("The model name already exists for this brand")
        average_price = self.request.data.get('average_price')
        if average_price is not None and int(average_price) <= 100000:
            raise ValidationError("The average price must be greater than 100,000")
        serializer.save(brand=brand)

# PATCH /models/<pk>/
class CarModelUpdateView(generics.UpdateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    lookup_url_kwarg = 'pk'

    def perform_update(self, serializer):
        average_price = self.request.data.get('average_price')
        if average_price is None or int(average_price) <= 100000:
            raise ValidationError("The average price must be greater than 100,000")
        serializer.save()

# GET /models?greater=&lower=
class CarModelListView(generics.ListAPIView):
    serializer_class = CarModelSerializer

    def get_queryset(self):
        queryset = CarModel.objects.all()
        greater = self.request.query_params.get('greater')
        lower = self.request.query_params.get('lower')
        if greater is not None:
            queryset = queryset.filter(average_price__gt=int(greater))
        if lower is not None:
            queryset = queryset.filter(average_price__lt=int(lower))
        return queryset
