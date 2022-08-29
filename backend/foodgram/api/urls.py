from django.urls import include, path
from rest_framework import routers

from .views import TagViewSet, IngredientViewSet, RecipeViewSet


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
