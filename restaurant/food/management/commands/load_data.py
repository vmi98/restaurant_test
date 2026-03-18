import csv

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from restaurant.food.models import Food, FoodCategory

FIXTURES_PATH = Path(settings.BASE_DIR) / 'restaurant' / 'fixtures'


class Command(BaseCommand):
    help = "Load food data from CSV"

    def handle(self, *args, **kwargs):
        self.load_categories()
        self.load_foods()
        self.stdout.write(self.style.SUCCESS("Data loaded successfully"))

    def load_categories(self):
        with open(FIXTURES_PATH / 'categories.csv', newline='',
                  encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                FoodCategory.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'name_ru': row['name_ru'],
                        'name_en': row['name_en'] or None,
                        'name_ch': row['name_ch'] or None,
                        'order_id': row['order_id'],
                    }
                )

    def load_foods(self):
        food_map = {}

        with open(FIXTURES_PATH / 'foods.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food = Food.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'category_id': row['category_id'],
                        'internal_code': row['internal_code'],
                        'code': row['code'],
                        'name_ru': row['name_ru'],
                        'description_ru': row['description_ru'],
                        'is_vegan': row['is_vegan'] == 'True',
                        'is_special': row['is_special'] == 'True',
                        'cost': row['cost'],
                        'is_publish': row['is_publish'] == 'True',
                    }
                )[0]

                food_map[row['internal_code']] = food

        with open(FIXTURES_PATH / 'foods.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['additional']:
                    current_food = food_map[row['internal_code']]
                    additional_ids = row['additional'].split(',')

                    for add_id in additional_ids:
                        if add_id in food_map:
                            current_food.additional.add(food_map[add_id])
