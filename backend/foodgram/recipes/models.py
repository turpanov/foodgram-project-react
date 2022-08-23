from django.db import models
from django.core.validators import MinValueValidator

from users.models import FoodgramUser



class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Тег')
    color = models.CharField(max_length=7, null=True, verbose_name='Цвет')
    slug = models.CharField(max_length=200, null=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        related_name='ingredients',
        verbose_name='Ингредиенты' 
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Текст')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1,
            message='Минимальное время приготовления: 1 мин.'
        )],
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
    

class RecipeIngredientAmount(models.Model):
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient_id = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators = [
            MinValueValidator(
                1,
                message = 'Минимальное количество: 1 ед.'
            ),
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient_id', 'recipe_id'],
                name='unique ingredient'
            ),
        )


class Favorite(models.Model):
    user_id = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Пользователь'
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=['user_id', 'recipe_id'],
                name='unique favorite'
            ),
        )


class ShoppingCart(models.Model):
    user_id = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name = 'shopping_cart',
        verbose_name='Пользователь'
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=['user_id', 'recipe_id'],
                name='unique shopping сart'
            ),
        )
