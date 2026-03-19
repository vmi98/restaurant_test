from django.db.models import Prefetch, QuerySet

from .models import Food, FoodCategory


def get_categories_with_published_foods() -> QuerySet[FoodCategory]:
    published_food = Food.objects.filter(is_publish=True
                                         ).order_by('internal_code', 'code')
    qs = FoodCategory.objects.prefetch_related(
        Prefetch("food", queryset=published_food)
    ).filter(food__is_publish=True).distinct().order_by('order_id', "id")
    return qs
