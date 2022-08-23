from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Follow

FoodgramUser = get_user_model()


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_is_subscribed(self, following):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=following).exists()


class FoodgramUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = FoodgramUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )