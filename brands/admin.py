from django.contrib import admin
from .models import Brand, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'average_price_display')
    inlines = [CarModelInline]

    def average_price_display(self, obj):
        return obj.average_price()
    average_price_display.short_description = 'Average Price'

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'average_price', 'brand')
    list_filter = ('brand',)

