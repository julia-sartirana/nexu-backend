from django.urls import path
from .views import (
    BrandListCreateView,
    BrandModelsListCreateView,
    CarModelUpdateView,
    CarModelListView,
)

urlpatterns = [
    path('brands/', BrandListCreateView.as_view(), name='brands_list_create'),
    path('brands/<int:brand_id>/models/', BrandModelsListCreateView.as_view(), name='brand_models_list_create'),
    path('models/<int:pk>/', CarModelUpdateView.as_view(), name='car_model_update'),
    path('models/', CarModelListView.as_view(), name='car_model_list'),
]
