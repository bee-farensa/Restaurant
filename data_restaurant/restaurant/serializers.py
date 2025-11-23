from rest_framework import serializers
from .models import Restaurant, Foodie, Review

class RestaurantSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'nama', 'lokasi', 'kategori', 'no_telp', 'deskripsi', 'total_reviews', 'average_rating']
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum([r.rating for r in reviews]) / len(reviews), 1)
        return 0

class FoodieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foodie
        fields = ['id', 'username', 'email', 'waktu']
        read_only_fields = ['id', 'waktu']

class ReviewSerializer(serializers.ModelSerializer):
    foodie_username = serializers.CharField(source='foodie.username', read_only=True)
    restaurant_nama = serializers.CharField(source='restaurant.nama', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'foodie', 'rating', 'komentar', 'waktu_review', 'foodie_username', 'restaurant_nama']
        read_only_fields = ['id', 'waktu_review']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['restaurant', 'foodie', 'rating', 'komentar']