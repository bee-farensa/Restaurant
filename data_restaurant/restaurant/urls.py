from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# DRF Router untuk API
router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant-api')
router.register(r'foodies', views.FoodieViewSet, basename='foodie-api')
router.register(r'reviews', views.ReviewViewSet, basename='review-api')

# Web URLs
web_patterns = [
    # Restaurant
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    
    # Foodie
    path('foodies/', views.FoodieListView.as_view(), name='foodie_list'),
    path('foodies/<int:pk>/', views.FoodieDetailView.as_view(), name='foodie_detail'),
    path('foodies/create/', views.FoodieCreateView.as_view(), name='foodie_create'),
    
    # Review
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_edit'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]

# API URLs
api_patterns = [
    path('api/', include(router.urls)),
]

urlpatterns = web_patterns + api_patterns