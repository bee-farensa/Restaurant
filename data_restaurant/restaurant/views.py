from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Restaurant, Foodie, Review
from .serializers import RestaurantSerializer, FoodieSerializer, ReviewSerializer



class RestaurantListView(ListView):
    """List semua restaurant - Read only untuk user"""
    model = Restaurant
    template_name = 'restaurant/restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 10


class RestaurantDetailView(DetailView):
    """Detail restaurant"""
    model = Restaurant
    template_name = 'restaurant/restaurant_detail.html'
    context_object_name = 'restaurant'


class FoodieListView(ListView):
    """List semua foodies"""
    model = Foodie
    template_name = 'restaurant/foodie_list.html'
    context_object_name = 'foodies'
    paginate_by = 10


class FoodieCreateView(CreateView):
    """Create foodie baru"""
    model = Foodie
    template_name = 'restaurant/foodie_form.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('foodie_list')
    
    def form_valid(self, form):
        # Cek username sudah ada
        if Foodie.objects.filter(username=form.cleaned_data['username']).exists():
            messages.error(self.request, "❌ Username sudah dipakai oleh foodie lain!")
            return self.form_invalid(form)
        
        # Cek email sudah ada
        if Foodie.objects.filter(email=form.cleaned_data['email']).exists():
            messages.error(self.request, "❌ Email sudah dipakai oleh foodie lain!")
            return self.form_invalid(form)
        
        messages.success(self.request, f"✅ Foodie '{form.cleaned_data['username']}' berhasil dibuat!")
        return super().form_valid(form)

class FoodieDetailView(DetailView):
    """Detail foodie"""
    model = Foodie
    template_name = 'restaurant/foodie_detail.html'
    context_object_name = 'foodie'

class ReviewListView(ListView):
    """List semua review dengan pagination"""
    model = Review
    template_name = 'restaurant/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10


class ReviewCreateView(CreateView):
    """Create review baru"""
    model = Review
    template_name = 'restaurant/review_form.html'
    fields = ['restaurant', 'foodie', 'rating', 'komentar']
    success_url = reverse_lazy('review_list')
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Review berhasil ditambahkan!")
        return super().form_valid(form)


class ReviewDetailView(DetailView):
    """Detail review"""
    model = Review
    template_name = 'restaurant/review_detail.html'
    context_object_name = 'review'


class ReviewUpdateView(UpdateView):
    """Update review (hanya milik foodie tersebut)"""
    model = Review
    template_name = 'restaurant/review_form.html'
    fields = ['rating', 'komentar']
    success_url = reverse_lazy('review_list')
    
    def get_object(self, queryset=None):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        # Di production, tambahkan permission check
        return review
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Review berhasil diperbarui!")
        return super().form_valid(form)


class ReviewDeleteView(DeleteView):
    """Delete review (hanya milik foodie tersebut)"""
    model = Review
    template_name = 'restaurant/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "✅ Review berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# ============ API VIEWSETS (DRF) ============

class RestaurantViewSet(viewsets.ModelViewSet):
    """API Restaurant - Read only"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    http_method_names = ['get', 'head', 'options']  # Hanya GET


class FoodieViewSet(viewsets.ModelViewSet):
    """API Foodie - Create & Read"""
    queryset = Foodie.objects.all()
    serializer_class = FoodieSerializer
    http_method_names = ['get', 'post', 'head', 'options']  # GET & POST only
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """API Review - Full CRUD"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_update(self, serializer):
        # Optional: Tambahkan logic untuk check owner review
        serializer.save()
    
    def perform_destroy(self, instance):
        # Optional: Tambahkan logic untuk check owner review
        instance.delete()