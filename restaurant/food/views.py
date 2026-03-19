from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from .models import FoodCategory
from .selectors import get_categories_with_published_foods
from .serializers import FoodListSerializer


class FoodListView(ListAPIView):
    serializer_class = FoodListSerializer

    def get_queryset(self) -> QuerySet[FoodCategory]:
        return get_categories_with_published_foods()
