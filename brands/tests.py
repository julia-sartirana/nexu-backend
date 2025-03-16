from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from brands.models import Brand, CarModel

class BrandTests(APITestCase):
    def test_create_brand(self):
        url = reverse('brands_list_create')
        data = {'name': 'Toyota'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(Brand.objects.get().name, 'Toyota')

    def test_duplicate_brand(self):
        Brand.objects.create(name='Toyota')
        url = reverse('brands_list_create')
        data = {'name': 'Toyota'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CarModelTests(APITestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Honda')

    def test_create_model(self):
        url = reverse('brand_models_list_create', kwargs={'brand_id': self.brand.id})
        data = {'name': 'Civic', 'average_price': 150000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CarModel.objects.count(), 1)
        self.assertEqual(CarModel.objects.get().name, 'Civic')

    def test_duplicate_model(self):
        CarModel.objects.create(name='Civic', average_price=150000, brand=self.brand)
        url = reverse('brand_models_list_create', kwargs={'brand_id': self.brand.id})
        data = {'name': 'Civic', 'average_price': 160000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_model(self):
        model_instance = CarModel.objects.create(name='Accord', average_price=200000, brand=self.brand)
        url = reverse('car_model_update', kwargs={'pk': model_instance.id})
        data = {'average_price': 250000}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        model_instance.refresh_from_db()
        self.assertEqual(model_instance.average_price, 250000)

