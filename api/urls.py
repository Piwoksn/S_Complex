from django.urls import path
from .views import ShopView, ProductDetailView, AllCartItemView, UserCartItemView, UserListView
from rest_framework.routers import SimpleRouter

route  = SimpleRouter()

route.register('user', UserListView, basename= ' user')




urlpatterns = [
    path('shop/<slug:pk>/', ShopView.as_view()),
    path('products/<uuid:pk>/', ProductDetailView.as_view()),
    path('cartitems/', AllCartItemView.as_view()),
    path('cartitems/<str:pk>/', UserCartItemView.as_view()),
] 

urlpatterns += route.urls