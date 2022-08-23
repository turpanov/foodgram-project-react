from django.contrib import admin
from .models import FoodgramUser


class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name', 'password')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'
    ordering = ['id']


admin.site.register(FoodgramUser, FoodgramUserAdmin)