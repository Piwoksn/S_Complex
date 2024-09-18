from rest_framework import serializers
from .models import Product, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "owner", "itemcategory",
                  "itemname", "itemimage", "itemimage2", "itemimage3", "itemvideo", "itemprice", "itemdiscount", "itemamount", "itemsize", "itemcolors", "itemdescription", "updated", "created", "paid"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "slug",
                  "image_url", "purchaser", "phone", "name", "price", "quantity", "size", "color", "added_at", "is_purchased", "total_price", "cart_image"]
