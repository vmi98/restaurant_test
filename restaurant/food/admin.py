from django.contrib import admin
from .models import FoodCategory, Food


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name_ru',
        'name_en',
        'name_ch',
        'order_id',
    )
    search_fields = (
        'name_ru',
        'name_en',
        'name_ch',
    )
    ordering = ('order_id', 'name_ru')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        'name_ru',
        'category',
        'cost',
        'is_publish',
        'is_vegan',
        'is_special',
    )
    list_filter = (
        'is_publish',
        'is_vegan',
        'is_special',
        'category',
    )
    search_fields = (
        'name_ru',
        'description_ru',
        'internal_code',
        'code',
    )
    autocomplete_fields = ('category', 'additional')