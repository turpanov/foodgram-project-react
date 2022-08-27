from rest_framework import viewsets

# from rest_framework.permissions import IsAdminUser
from .paginator import FoodgramPagePagination
from .permissions import OwnerOrAdminOrReadOnly
from recipes.models import Tag, Ingredient, Recipe
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeIngredientAmountSerializer,
    RecipeGetSerializer,
    RecipePostSerializer
)

from .filters import IngredientFilter


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer