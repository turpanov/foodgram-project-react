from django.urls import include, path
from rest_framework import routers

from .views import FoodgramUserViewSet

router = routers.DefaultRouter()
router.register(r'users', FoodgramUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]