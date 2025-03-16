import json
import os
from django.core.management.base import BaseCommand
from brands.models import Brand, CarModel

class Command(BaseCommand):
    help = 'Populate the database from the models.json file (optimized with bulk_create)'

    def handle(self, *args, **options):
        # Adjust the path according to the location of models.json; here it is assumed to be in the project root
        file_path = os.path.join(os.path.dirname(__file__), '../../utils/models.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading the JSON file: {e}'))
            return

        # Extract unique brand names from the JSON (case-insensitive)
        brand_names = set()
        for item in data:
            brand_name = item.get('brand_name')
            if brand_name:
                brand_names.add(brand_name.strip())

        # Query for existing brands
        existing_brands = Brand.objects.filter(name__in=brand_names)
        existing_brand_names = set(b.name for b in existing_brands)

        # Create missing brands using bulk_create
        missing_brands = [Brand(name=name) for name in brand_names if name not in existing_brand_names]
        if missing_brands:
            Brand.objects.bulk_create(missing_brands)
            self.stdout.write(self.style.SUCCESS(f'Created {len(missing_brands)} new brands.'))

        # Reload all brands (existing + newly created) and map them
        brands = Brand.objects.filter(name__in=brand_names)
        brand_map = {b.name: b for b in brands}

        # Query for existing models to avoid duplicates.
        # Create a set of tuples (brand.lower(), model.lower())
        existing_models = CarModel.objects.filter(brand__name__in=brand_names)
        existing_models_set = {(cm.brand.name.lower(), cm.name.lower()) for cm in existing_models}

        # Accumulate new CarModel objects to create
        new_models = []
        for item in data:
            brand_name = item.get('brand_name')
            model_name = item.get('name')
            average_price = item.get('average_price')

            if not (brand_name and model_name):
                continue

            key = (brand_name.lower(), model_name.lower())
            if key not in existing_models_set:
                brand = brand_map.get(brand_name.strip())
                # Add the new model; if average_price is 0 or None, it is created as per the JSON
                new_models.append(CarModel(
                    name=model_name,
                    average_price=average_price,
                    brand=brand
                ))
                existing_models_set.add(key)  # Avoid duplicates if the JSON contains repeated entries

        if new_models:
            CarModel.objects.bulk_create(new_models)
            self.stdout.write(self.style.SUCCESS(f'Bulk created {len(new_models)} new models.'))
        else:
            self.stdout.write(self.style.SUCCESS('No new models found to insert.'))

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
