from django import forms
from .models import Restaurant, Review, Foodie

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['nama', 'lokasi', 'kategori', 'no_telp', 'deskripsi']

class ReviewForm(forms.ModelForm):
    # Custom fields (tidak ada di model Review)
    nama = forms.CharField(max_length=150, label='Nama Kamu')
    email = forms.EmailField(label='Email Kamu')
    
    class Meta:
        model = Review
        fields = ['rating', 'komentar']  # Field dari model Review
    
    # Override method save untuk handle Foodie
    def save(self, restaurant, commit=True):
        review = super().save(commit=False)
        review.restaurant = restaurant
        
        # Get or create Foodie
        foodie, created = Foodie.objects.get_or_create(
            username=self.cleaned_data['nama'],
            defaults={'email': self.cleaned_data['email']}
        )
        
        if not created and foodie.email != self.cleaned_data['email']:
            foodie.email = self.cleaned_data['email']
            foodie.save()
        
        review.foodie = foodie
        
        if commit:
            review.save()
        return review
    
class FoodieForm(forms.ModelForm):
    nama = forms.CharField(max_length=150, label='Nama Kamu')
    email = forms.EmailField(label='Email Kamu')

    class Meta:
        model = Foodie
        fields = ['nama', 'email']

    def save(self, commit=True):
        username = self.cleaned_data['nama']
        email = self.cleaned_data['email']

        foodie, created = Foodie.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )

        # Kalau username sudah ada tapi email berubah → update
        if not created and foodie.email != email:
            foodie.email = email
            foodie.save()

        return foodie