from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer, CartItemSerializer
from django.contrib.auth import get_user_model

# Create your views here.
class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
