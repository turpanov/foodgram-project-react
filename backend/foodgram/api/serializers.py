from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    ShoppingCart,
    Tag
)
from users.models import Follow


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
        return Follow.objects.filter(
            user=request.user,
            following=following
        ).exists()


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
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        if Follow.objects.filter(
                user=self.context['request'].user,
                following=data['following']
        ):
            raise serializers.ValidationError('Подписка уже оформлена.')
        return data

    def to_representation(self, instance):
        return ListFollowRecipeSerializer(
            instance.following,
            context={'request': self.context.get('request')}
        ).data


class ListFollowRecipeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, following):
        return Recipe.objects.filter(author=following).count()

    def get_recipes(self, following):
        queryset = self.context['request']
        recipes_limit = queryset.query_params.get('recipes_limit')
        if not recipes_limit:
            return FollowRecipeSerializer(
                following.author.all(),
                many=True, context={'request': queryset}
            ).data
        return FollowRecipeSerializer(
            following.author.all()[:int(recipes_limit)], many=True,
            context={'request': self.context['request']}
        ).data

    def get_is_subscribed(self, following):
        return Follow.objects.filter(
            user=self.context.get('request').user,
            following=following
        ).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source='ingredient_id.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient_id.measurement_unit',
        read_only=True
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient_id.id',
        read_only=True
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeGetSerializer(serializers.ModelSerializer):
    author = FoodgramUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, recipe):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        is_favorited = Favorite.objects.filter(
            user_id=request.user,
            recipe_id=recipe
        ).exists()
        return is_favorited

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        is_in_shopping_cart = ShoppingCart.objects.filter(
            user_id=request.user,
            recipe_id=recipe
        ).exists()
        return is_in_shopping_cart

    def get_ingredients(self, recipe):
        return RecipeIngredientAmountSerializer(
            RecipeIngredientAmount.objects.filter(recipe_id=recipe),
            many=True
        ).data


class RecipePostSerializer(serializers.ModelSerializer):
    author = FoodgramUserSerializer(read_only=True)
    ingredients = RecipeIngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться'
                })
            ingredients_list.append(ingredient['id'])
        data['ingredients'] = ingredients
        return data

    def ingredient_tags_create(self, recipe, ingredients, tags):
        RecipeIngredientAmount.objects.bulk_create(
            [RecipeIngredientAmount(
                ingredient_id=get_object_or_404(
                    Ingredient,
                    id=ingredient_item.get('id')
                ),
                recipe_id=recipe,
                amount=ingredient_item.get('amount')
            ) for ingredient_item in ingredients]
        )
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
        self.ingredient_tags_create(recipe, ingredients, tags)
        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe.tags.clear()
        recipe.ingredients.clear()
        recipe.tags.set(tags)
        self.ingredient_tags_create(recipe, ingredients, tags)
        recipe.save()
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(
            instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipeValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user_id', 'recipe_id')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = self.context.get('recipe')
        favorite_recipe = Favorite.objects.filter(
            user_id=user,
            recipe_id=recipe
        )
        if request.method == 'POST':
            if favorite_recipe.exists():
                raise serializers.ValidationError({
                    'error': 'Рецепт уже добавлен в избранное.'
                })
        if request.method == 'DELETE':
            if not favorite_recipe.exists():
                raise serializers.ValidationError({
                    'error': 'Рецепта нет в избранном.'
                })
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user_id', 'recipe_id')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = data['recipe_id']
        shopping_cart_recipe = ShoppingCart.objects.filter(
            user_id=user,
            recipe_id=recipe
        )
        if request.method == 'POST':
            if shopping_cart_recipe.exists():
                raise serializers.ValidationError({
                    'error': 'Рецепт уже добавлен в корзину.'
                })
        if request.method == 'DELETE':
            if not shopping_cart_recipe.exists():
                raise serializers.ValidationError({
                    'error': 'Рецепта нет в корзине.'
                })
        return data
