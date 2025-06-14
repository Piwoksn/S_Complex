from rest_framework import serializers
from django.contrib.auth import get_user_model
from shopapp.models import Product, CartItem

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("id", "profilepic", "moredesc",
                  "businessname", "slug", "country", "phone", "email", "meansofid", "idnumber", "idpic", "logo", "currency", "coins", "whatsapp", "username", "password", "updated", "created", "subscribed", "date", "trial_start", "trial_end")

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ("id", "owner", "itemcategory", "itemname", "itemimage", "itemimage2", "itemimage3", "itemvideo", "itemprice", "itemdiscount", "itemamount", "itemsize", "itemcolors", "itemdescription", "updated", "created", "paid")


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ("id", "product", "slug", "image_url", "purchaser", "phone", "name", "price", "quantity", "size", "color", "added_at", "is_purchased", "total_price", "cart_image")


