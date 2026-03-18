from rest_framework.generics import ListAPIView
from .serializers import FoodListSerializer
from .models import Food

class FoodListView(ListAPIView):
    serializer_class = FoodListSerializer
    queryset = Food.objects.all()
