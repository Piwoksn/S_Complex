from django.urls import path
from . import views


urlpatterns = [
    path('shop/<str:pk>/', views.shop, name='shop'),
    path('product/<str:pk>/', views.product, name='product'),

    path('cart/<str:user_slug>/', views.view_cart, name='cart'),

    path('addProduct/', views.addProduct, name='addProduct'),
    path('remove_from_cart/<str:product_id>',
         views.remove_from_cart, name='remove_from_cart'),
    path('place_order/<str:user_slug>/', views.place_order, name='place_order'),
    path('purchase_item/<str:pk>/', views.purchase_item, name='purchase_item'),

    path('search/<str:pk>/', views.search, name='search'),



    # path('clear_cart/', views.clear_cart, name='clear_cart'),  # Uncomment this line

    # ----------Django Rest Framework For Product------------------
    path('product/', views.ProductPostListCreate.as_view(), name="product"),
    path('product/<int:pk>',
         views.ProductRetrieveUpdateDestroy.as_view(), name="productupdate"),
    #     ------------End REst Framework-----

    # ----------Django Rest Framework For Cart Item------------------
    path('cart/', views.CartItemPostListCreate.as_view(), name="cart"),
    path('cart/<int:pk>',
         views.CartItemRetrieveUpdateDestroy.as_view(), name="cartitem"),
    #     ------------End REst Framework-----
]
