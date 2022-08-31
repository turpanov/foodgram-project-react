from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    ShoppingCart,
    Tag
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'image')
    readonly_fields = ('added_to_favorite_count',)
    search_fields = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def added_to_favorite_count(self, obj):
        return obj.favorited.count()

    added_to_favorite_count.short_description = (
        'Количество добавлений в избранное'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    ordering = ['id']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')
    search_fields = ('user_id', 'recipe_id')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')
    search_fields = ('user_id', 'recipe_id')
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredientAmount)
class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe_id', 'ingredient_id', 'amount')
    search_fields = ('recipe_id', 'ingredient_id')
    empty_value_display = '-пусто-'
