from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer, CartItemSerializer
from django.contrib.auth import get_user_model
from shopapp.models import Product, CartItem

# Create your views here.
class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    
    def form_valid(self, form):
        form.instance.logo = self.request.user.logo
        form.save()
        
        return super().form_valid(self, form)


class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()