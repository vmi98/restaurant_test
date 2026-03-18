from rest_framework.generics import ListAPIView

from .models import Food
from .serializers import FoodListSerializer


class FoodListView(ListAPIView):
    serializer_class = FoodListSerializer
    queryset = Food.objects.all()
