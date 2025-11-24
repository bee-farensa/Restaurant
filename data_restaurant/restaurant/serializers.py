from rest_framework import serializers
from .models import Restaurant, Foodie, Review

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'nama', 'lokasi', 'kategori', 'no_telp', 'deskripsi']


class FoodieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foodie
        fields = ['id', 'username', 'email', 'waktu']
    
    def validate_username(self, value):
        # Validasi username belum dipakai (exclude id saat update)
        qs = Foodie.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Username sudah dipakai oleh foodie lain!")
        return value
    
    def validate_email(self, value):
        # Validasi email belum dipakai (exclude id saat update)
        qs = Foodie.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Email sudah dipakai oleh foodie lain!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    foodie_username = serializers.CharField(source='foodie.username', read_only=True)
    restaurant_nama = serializers.CharField(source='restaurant.nama', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'foodie', 'restaurant_nama', 'foodie_username', 
                  'rating', 'komentar', 'waktu_review']
    