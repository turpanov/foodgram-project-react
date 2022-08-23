from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import FoodgramUserSerializer
from api.paginator import FoodgramPagePagination


FoodgramUser = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer
    pagination_class = FoodgramPagePagination
