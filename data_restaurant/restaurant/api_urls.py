from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, FoodieViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='api-restaurant')
router.register(r'foodies', FoodieViewSet, basename='api-foodie')
router.register(r'reviews', ReviewViewSet, basename='api-review')

urlpatterns = [
    path('', include(router.urls)),
]