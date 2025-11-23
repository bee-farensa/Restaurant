from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Restaurant
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/review/', views.submit_review, name='submit_review'),
    
    # Foodie
    path('foodies/', views.foodie_list, name='foodie_list'),
    path('foodie/<int:id>/', views.foodie_detail, name='foodie_detail'),
    
    # Review
    path('reviews/', views.review_list, name='review_list'),
    path('review/<int:id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:id>/delete/', views.delete_review, name='delete_review'),
]