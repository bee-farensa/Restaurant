from django.contrib import admin
from .models import Restaurant, Foodie, Review

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kategori', 'lokasi', 'no_telp']
    list_filter = ['kategori']
    search_fields = ['nama', 'lokasi']

@admin.register(Foodie)
class FoodieAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'waktu']
    search_fields = ['username', 'email']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['foodie', 'restaurant', 'rating', 'waktu_review']
    list_filter = ['rating', 'waktu_review']
    search_fields = ['foodie__username', 'restaurant__nama']