from django.contrib import admin

from .models import Recipe, Ingredient, Favorite, RecipeIngredientAmount, ShoppingCart, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def added_to_favorite_count(self, obj):
        return obj.favorite.count()
    

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    ordering = ['id']


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')
    search_fields = ('user_id', 'recipe_id')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')
    search_fields = ('user_id', 'recipe_id')
    empty_value_display = '-пусто-'


class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe_id', 'ingredient_id', 'amount')
    search_fields = ('recipe_id', 'ingredient_id')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(RecipeIngredientAmount, RecipeIngredientAmountAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)