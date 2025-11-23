from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Restaurant, Foodie, Review
from rest_framework import viewsets
from .serializers import RestaurantSerializer, FoodieSerializer, ReviewSerializer, ReviewCreateSerializer
from .forms import FoodieForm, ReviewForm

# Homepage - List Restoran
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/restaurant_list.html', {'restaurants': restaurants})

# Detail Restoran + Reviews
def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    reviews = restaurant.reviews.all()
    return render(request, 'restaurant/restaurant_detail.html', {
        'restaurant': restaurant,
        'reviews': reviews
    })

# Submit Review
def review_form(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        komentar = request.POST.get('komentar')
        
        # Cari atau buat Foodie
        foodie, created = Foodie.objects.get_or_create(
            username=nama,
            defaults={'email': email}
        )
        
        # Update email kalau berbeda
        if not created and foodie.email != email:
            foodie.email = email
            foodie.save()
        
        # Buat review
        Review.objects.create(
            restaurant=restaurant,
            foodie=foodie,
            rating=rating,
            komentar=komentar
        )
        
        messages.success(request, f'Review berhasil ditambahkan! Terima kasih, {nama}!')
        return redirect('restaurant_detail', id=restaurant_id)
    
    return render(request, 'restaurant/review_form.html', {'restaurant': restaurant})

# List Semua Foodie
def foodie_list(request):
    foodies = Foodie.objects.all().order_by('-waktu')
    return render(request, 'restaurant/foodie_list.html', {'foodies': foodies})

def foodie_form(request):
    if request.method == 'POST':
        form = FoodieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Akun berhasil dibuat! Selamat datang, {form.cleaned_data["username"]}!')
            return redirect('foodie_list')
    else:
        form = FoodieForm()
    
    return render(request, 'restaurant/register_foodie.html', {'form': form})

# Profile Foodie
def foodie_detail(request, id):
    foodie = get_object_or_404(Foodie, id=id)
    reviews = foodie.reviews.all()
    return render(request, 'restaurant/foodie_detail.html', {
        'foodie': foodie,
        'reviews': reviews
    })

# List Semua Review
def review_list(request):
    reviews = Review.objects.all().order_by('-waktu_review')
    return render(request, 'restaurant/review_list.html', {'reviews': reviews})

# Edit Review
def edit_review(request, id):
    review = get_object_or_404(Review, id=id)
    
    if request.method == 'POST':
        # Update data review
        review.rating = request.POST.get('rating')
        review.komentar = request.POST.get('komentar')
        
        # Update nama & email foodie
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        
        if review.foodie.username != nama or review.foodie.email != email:
            # Cek apakah nama baru sudah ada
            existing_foodie = Foodie.objects.filter(username=nama).exclude(id=review.foodie.id).first()
            
            if existing_foodie:
                messages.error(request, f'Nama "{nama}" sudah dipakai oleh orang lain!')
                return redirect('edit_review', id=id)
            else:
                # Update foodie yang ada
                review.foodie.username = nama
                review.foodie.email = email
                review.foodie.save()
        
        review.save()
        messages.success(request, 'Review berhasil diupdate!')
        return redirect('restaurant_detail', id=review.restaurant.id)
    
    return render(request, 'restaurant/edit_review.html', {'review': review})

# Delete Review
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    restaurant_id = review.restaurant.id
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review berhasil dihapus!')
        return redirect('restaurant_detail', id=restaurant_id)
    
    return render(request, 'restaurant/delete_review.html', {'review': review})


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class FoodieViewSet(viewsets.ModelViewSet):
    queryset = Foodie.objects.all()
    serializer_class = FoodieSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer