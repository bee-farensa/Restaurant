from django.db import models

# Restaurant Model
class Restaurant(models.Model):
    KATEGORI_CHOICES = [
        ('kafe', 'Cafe'),
        ('fine_dining', 'Fine Dining Restaurant'),
        ('casual_dining', 'Casual Dining Restaurant'),
        ('fast_casual', 'Fast Casual Dining'),
        ('fast_food', 'Fast Food Restaurant'),
    ]
    
    nama = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=200)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    no_telp = models.CharField(max_length=20)
    deskripsi = models.TextField()
    
    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = "Restaurants"


# Foodie Model (TANPA PASSWORD)
class Foodie(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    waktu = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Foodies"


# Review Model
class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    foodie = models.ForeignKey(Foodie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    komentar = models.TextField()
    waktu_review = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.foodie.username} - {self.restaurant.nama} ({self.rating}⭐)"
    
    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ['-waktu_review']