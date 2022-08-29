from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .utils import download_shopping_cart
from .paginator import FoodgramPagePagination
from .permissions import OwnerOrAdminOrReadOnly
from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, RecipeIngredientAmount
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeIngredientAmountSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    FavoriteRecipeValidationSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    ShoppingCartValidationSerializer

)

from .filters import IngredientFilter, RecipeFilter


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    pagination_class = FoodgramPagePagination
    permission_classes = (OwnerOrAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            'recipe_id': pk,
            'user_id': user.id
        }
        serializer = FavoriteRecipeValidationSerializer(
            data=data,
            context={
                'request': request,
                'recipe': recipe
            },
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            Favorite.objects.create(user_id=user, recipe_id=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        favorite_recipe = Favorite.objects.filter(
            user_id=user,
            recipe_id=recipe
        )
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            'recipe_id': pk,
            'user_id': user.id
        }
        serializer = ShoppingCartValidationSerializer(
            data=data,
            context={
                'request': request,
                'recipe': recipe
            },
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            ShoppingCart.objects.create(user_id=user, recipe_id=recipe)
            serializer = ShoppingCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        shopping_cart_recipe = ShoppingCart.objects.filter(
            user_id=user,
            recipe_id=recipe
        )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        recipe_ingredient = RecipeIngredientAmount.objects.filter(
            recipe_id__shopping_cart__user_id=request.user
        )
        return download_shopping_cart(recipe_ingredient)