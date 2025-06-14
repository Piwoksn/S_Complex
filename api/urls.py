from django.urls import path
from .views import UserView, UserDetailView, ProductListView, ProductDetailView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<uuid:pk>/', ProductDetailView.as_view()),
]