from rest_framework.generics import ListAPIView

from .selectors import get_categories_with_published_foods
from .serializers import FoodListSerializer


class FoodListView(ListAPIView):
    serializer_class = FoodListSerializer

    def get_queryset(self):
        return get_categories_with_published_foods()
