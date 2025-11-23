from django.contrib import admin
from .models import Restaurant, Foodie, Review


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kategori', 'lokasi', 'no_telp')
    search_fields = ('nama', 'lokasi')
    list_filter = ('kategori',)
    fieldsets = (
        ('Informasi Umum', {
            'fields': ('nama', 'kategori')
        }),
        ('Kontak & Lokasi', {
            'fields': ('lokasi', 'no_telp')
        }),
        ('Deskripsi', {
            'fields': ('deskripsi',),
            'classes': ('wide',)
        }),
    )


@admin.register(Foodie)
class FoodieAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'waktu', 'jumlah_review')
    search_fields = ('username', 'email')
    readonly_fields = ('waktu',)
    fieldsets = (
        ('Data Foodie', {
            'fields': ('username', 'email')
        }),
        ('Timestamp', {
            'fields': ('waktu',)
        }),
    )
    
    def jumlah_review(self, obj):
        return obj.reviews.count()
    jumlah_review.short_description = 'Jumlah Review'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('foodie', 'restaurant', 'rating_stars', 'waktu_review')
    search_fields = ('foodie__username', 'restaurant__nama')
    list_filter = ('rating', 'waktu_review')
    readonly_fields = ('waktu_review',)
    fieldsets = (
        ('Data Review', {
            'fields': ('restaurant', 'foodie')
        }),
        ('Review Content', {
            'fields': ('rating', 'komentar'),
            'classes': ('wide',)
        }),
        ('Timestamp', {
            'fields': ('waktu_review',)
        }),
    )
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating + '☆' * (5 - obj.rating)
        return f"{stars} ({obj.rating}/5)"
    rating_stars.short_description = 'Rating'