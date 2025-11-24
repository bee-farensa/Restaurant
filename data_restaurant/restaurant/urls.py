from django.urls import path
from . import views

urlpatterns = [
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
