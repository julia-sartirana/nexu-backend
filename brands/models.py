from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def average_price(self):
        car_models = self.models.all()
        if car_models.exists():
            total = sum([m.average_price for m in car_models])
            return round(total / car_models.count())
        return 0

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=255)
    average_price = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, related_name='models', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'brand')

    def __str__(self):
        return f"{self.name} ({self.brand.name})"

