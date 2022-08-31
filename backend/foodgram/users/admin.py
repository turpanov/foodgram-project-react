from django.contrib import admin

from .models import Follow, FoodgramUser


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
        'password'
    )
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'
    ordering = ['id']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user', 'following')
    empty_value_display = '-пусто-'
    ordering = ['id']
