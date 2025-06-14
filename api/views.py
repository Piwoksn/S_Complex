from rest_framework import generics, viewsets
from .serializers import UserSerializer, ProductSerializer, CartItemSerializer
from django.contrib.auth import get_user_model
from shopapp.models import Product, CartItem
from .permissions import UserPermission
from rest_framework import permissions

# Create your views here.
class UserListView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [UserPermission, permissions.IsAuthenticated]


class ShopView(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        slug = self.kwargs.get('pk')
        store = Product.objects.filter(owner__slug = slug)
        return store
    

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class AllCartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

class UserCartItemView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        owner = self.kwargs.get('pk')
        cart = CartItem.objects.filter(product__owner__slug = owner)
        return cart