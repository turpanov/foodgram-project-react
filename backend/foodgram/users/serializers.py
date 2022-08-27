from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'following')
    
    def validate(self, data):
        get_object_or_404(FoodgramUser, username=data['following'])
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError('Сам на себя подписываешься!')
        if Follow.objects.filter(
                user=self.context['request'].user,
                following=data['following']
        ):
            raise serializers.ValidationError('Уже подписан')
        return data

    # def to_representation(self, instance):
    #     return FollowListSerializer(
    #         instance.following,
    #         context={'request': self.context.get('request')}
    #     ).data
