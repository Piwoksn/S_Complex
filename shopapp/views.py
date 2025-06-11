
from django.db.models.functions import Concat
from django.db.models import Value
from django.http import HttpResponse
from django.utils import timezone


from django.shortcuts import HttpResponseRedirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from .utils import calculate_cart_total
import json
import os
import mimetypes
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import User
from .models import Product, CartItem
import uuid
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
import requests
from io import BytesIO
from PIL import Image
from django.conf import settings
# Search bar import
from django.db.models import Q

# Rest_FrameWork imports
from rest_framework import generics, status
from .serializers import ProductSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# ... other view functions ...


# ...
# Main Backup
def place_order(request, user_slug):

    user = User.objects.get(slug=user_slug)

    if request.method == 'POST':
        # Retrieve the cart data from the cookie
        cart_json = request.COOKIES.get('cart', '[]')
        cart = json.loads(cart_json)

        # Create a list to store the details of cart items
        cart_items = []

        # Loop through the cart items and retrieve their details
        for cart_item in cart:
            product_id = cart_item.get('product_id')
            name = cart_item.get('name')
            price = cart_item.get('price')
            quantity = cart_item.get('quantity')
            size = cart_item.get('size')
            color = cart_item.get('color')
            image_url = cart_item.get('image')

            # Fetch the Product object to access the image from the model
            shop_item = get_object_or_404(Product, pk=product_id)

            # Create a dictionary representing the cart item
            cart_items.append({
                'product_id': product_id,
                'name': name,
                'price': price,
                'quantity': quantity,
                'size': size,
                'color': color,
                # Use Product's image URL
                'image_url': shop_item.itemimage.url[8:],
            })

        # Calculate the cart total using the calculate_cart_total function
        cart_total = calculate_cart_total(cart_items)

        if request.method == 'POST':
            # For anonymous users, retrieve purchaser and phone from the form
            purchaser = request.POST.get('purchaser', '')
            phone = request.POST.get('phone', '')

            # Create a new CartItem object and save it to the database for each cart item
            for cart_item in cart_items:
                CartItem.objects.create(
                    product_id=cart_item['product_id'],
                    purchaser=purchaser,
                    phone=phone,
                    name=cart_item['name'],
                    price=cart_item['price'],
                    quantity=cart_item['quantity'],
                    size=cart_item['size'],
                    color=cart_item['color'],
                    image_url=cart_item['image_url'],
                    cart_image=cart_item['image_url'],
                    total_price=float(
                        cart_item['price']) * int(cart_item['quantity']),
                    slug=user.slug,
                )

            # Clear the cart data from the cookie after placing the order
            response = HttpResponseRedirect(
                reverse('shop', kwargs={'pk': user.slug}))
            response.delete_cookie('cart')  # Clear the 'cart' cookie

            # Add a success message
            messages.success(
                request, 'Your order has been received. You will be contacted shortly. Thank You')

            return response

    # Handle the case when the form is not submitted (GET request)
    else:
        return HttpResponseBadRequest("Invalid request method")


# Inside your 'view_cart' view
def view_cart(request, user_slug):
    # Retrieve the user based on the provided slug
    user = User.objects.get(slug=user_slug)

    # Retrieve the cart data from the 'cart' cookie
    cart = request.COOKIES.get('cart', '[]')
    cart = json.loads(cart)

    # Create a list to store the details of cart items
    cart_items = []

    # Loop through the cart items and retrieve their details
    for cart_item in cart:
        product_id = cart_item.get('product_id')
        name = cart_item.get('name')
        price = cart_item.get('price')
        quantity = cart_item.get('quantity')
        size = cart_item.get('size')
        color = cart_item.get('color')
        image_url = cart_item.get('image')  # Include the image URL

        # Create a dictionary representing the cart item
        cart_items.append({
            'product_id': product_id,
            'name': name,
            'price': price,
            'quantity': quantity,
            'size': size,
            'color': color,
            'image_url': image_url,
        })

    # Calculate the cart total using the calculate_cart_total function
    cart_total = calculate_cart_total(cart_items)
    # Update the cart count in the context
    cart_count = len(cart)

    context = {
        'user': user,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,

    }

    return render(request, 'shopapp/cart.html', context)


def product(request, pk):
    shop = Product.objects.get(id=pk)
    user = shop.owner

    size = shop.itemsize.split()
    colour = shop.itemcolors.split()

    context = {'size': size, 'colour': colour,
               'user': user, 'shopproduct': shop}

    # Initialize the cart as an empty list if it doesn't exist in the cookies
    cart = request.COOKIES.get('cart', '[]')
    cart = json.loads(cart)

    if request.method == 'POST':
        name = request.POST.get('itemname')
        price = request.POST.get('itemamount')
        quantity = request.POST.get('itemquantity')
        size = request.POST.get('itemsize')
        color = request.POST.get('itemcolors')

        # Build the path to the image within the media directory
        image_filename = os.path.basename(shop.itemimage.name)
        image_path = os.path.join('static', 'images', 'media', image_filename)

        # Check if the image file exists
        if os.path.exists(image_path):
            # Determine the content type based on the file extension
            file_extension = os.path.splitext(image_filename)[-1].lower()

            # Use the mimetypes module to guess the content type based on the file extension
            content_type, _ = mimetypes.guess_type(image_filename)

            # If the content type is not determined or not supported, set a default content type
            if not content_type or not content_type.startswith('image/'):
                content_type = 'image/*'

            # Read the image data from the file
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            # Create a file object with the determined content type
            cart_image = SimpleUploadedFile(
                image_filename, image_data, content_type=content_type)

            # Calculate total_price (assuming Product model has a price field)
            total_price = float(price) * int(quantity)

            # Create a dictionary representing the cart item
            cart_item = {
                'product_id': pk,
                'name': name,
                'price': price,
                'quantity': quantity,
                'size': size,
                'color': color,
                'image': shop.itemimage.url,  # Include the image URL
            }

            # Append the cart item to the cart list in cookies
            cart.append(cart_item)

            # Update the cart count in the context
            cart_count = len(cart)
            context['cart_count'] = cart_count

            # Serialize the cart list to JSON and store it in a cookie
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            response.set_cookie('cart', json.dumps(cart), max_age=None)

            messages.success(request, 'Item added to cart successfully.')
            return response
        else:
            # Handle the case where the image file doesn't exist
            return HttpResponseNotFound("Image not found")

    # When the user clicks "Make Order," transfer items to the database
    if request.method == 'GET' and 'make_order' in request.GET:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Loop through the items in the cart and save them to the database
            for cart_item in cart:
                # Create a CartItem object and save it to the database
                new_cart_item = CartItem(
                    cart_owner=request.user,
                    product=Product.objects.get(pk=cart_item['product_id']),
                    name=cart_item['name'],
                    price=cart_item['price'],
                    quantity=cart_item['quantity'],
                    size=cart_item['size'],
                    color=cart_item['color'],
                    total_price=float(
                        cart_item['price']) * int(cart_item['quantity']),
                )
                new_cart_item.save()

            # Clear the cart in cookies
            # No need to delete the 'cart' cookie here, as we want to retain the selected items
            messages.success(request, 'Order placed successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'You need to log in to place an order.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Update the cart count in the context
    cart_count = len(cart)
    context['cart_count'] = cart_count

    return render(request, 'shopapp/product.html', context)


def remove_from_cart(request, product_id):
    # Retrieve the cart data from the 'cart' cookie
    cart_json = request.COOKIES.get('cart', '[]')
    cart = json.loads(cart_json)

    # Find the index of the item with the given product_id in the cart
    index_to_remove = None
    for index, cart_item in enumerate(cart):
        if cart_item.get('product_id') == product_id:
            index_to_remove = index
            break

    # If the item is found, remove it from the cart
    if index_to_remove is not None:
        del cart[index_to_remove]

        # Update the 'cart' cookie with the modified cart data
        cart_json = json.dumps(cart)  # Convert the cart back to JSON
        max_age = None  # To make the cookie last for the duration of the session

        # Set the 'cart' cookie with the updated cart data
        response = HttpResponseRedirect(
            request.META.get('HTTP_REFERER', 'shopapp:index'))
        response.set_cookie('cart', cart_json, max_age=max_age)

        messages.success(request, 'Item removed from cart')

    else:
        # If the item was not found, display a warning message
        messages.warning(request, 'Item not found in cart')

    # Redirect back to the cart page
    return response


def shop(request, pk):
    try:
        user = get_object_or_404(User, slug=pk)
        shop = Product.objects.filter(owner=user)
        categories = shop.values('itemcategory').distinct()

        # Initialize the cart as an empty list if it doesn't exist in the cookies
        cart = request.COOKIES.get('cart', '[]')
        cart = json.loads(cart)

        # Update the cart count in the context
        cart_count = len(cart)

        # Check if the 'product_id' query parameter is in the URL
        product_id = request.GET.get('product_id')

        context = {
            'user': user,
            'shop': shop,
            'categories': categories,
            'cart_count': cart_count,
        }

        return render(request, 'shopapp/shop.html', context)

    except Exception:
        return HttpResponse('Page not available')

# main view
# def shop(request, pk):
#     try:
#         user = get_object_or_404(User, slug=pk)
#         shop = Product.objects.filter(owner=user)
#         categories = shop.values('itemcategory').distinct()

#         # Initialize the cart as an empty list if it doesn't exist in the cookies
#         cart = request.COOKIES.get('cart', '[]')
#         cart = json.loads(cart)

#         # Update the cart count in the context
#         cart_count = len(cart)

#         # Calculate discount price and percentage for each product in the shop
#         # for item in shop:
#         #     if item.itemdiscount:
#         #         discountprice = item.itemprice-item.itemdiscount
#         #         discountpercentage = int(
#         #             (item.itemdiscount/item.itemprice)*100)
#         #         print(discountpercentage)
#         #     else:
#         #         discountprice = None
#         #         discountpercentage = None

#         context = {
#             'user': user,
#             'shop': shop,
#             'categories': categories,
#             'cart_count': cart_count,
#             # 'discountprice': discountprice,
#             # 'discountpercentage': discountpercentage,
#         }
#     except Exception:
#         return HttpResponse('Page not available')

#     return render(request, 'shopapp/shop.html', context)


@login_required(login_url='loginform')
def addProduct(request):
    user = request.user
    if request.method == 'POST':
        # try:
        category = request.POST.get('category')
        itemimage = request.FILES.get('itemimage')
        itemimage2 = request.FILES.get('itemimage2')
        itemimage3 = request.FILES.get('itemimage3')
        itemvideo = request.FILES.get('itemvideo4')
        itemname = request.POST.get('itemname')
        itemprice = request.POST.get('itemprice')
        itemdiscount = request.POST.get('itemdiscount')
        itemcolours = request.POST.get('itemcolour')
        itemsize = request.POST.get('itemsize')
        itemdescription = request.POST.get('itemdescription')

        if itemdiscount != 0:
            amount = float(itemprice)-float(itemdiscount)

        else:
            amount = itemprice

        Product.objects.create(owner=user, itemcategory=category, itemimage=itemimage, itemimage2=itemimage2, itemimage3=itemimage3, itemvideo=itemvideo, itemname=itemname, itemprice=itemprice, itemdiscount=itemdiscount,
                                itemamount=amount, itemcolors=itemcolours, itemsize=itemsize, itemdescription=itemdescription)

        messages.success(request, 'Successfully uploaded to shop')
        return redirect('portal')
        # except:
        #     messages.warning(
        #         request, 'an error occured, field must not be empty')
        #     return redirect('portal')

    else:
        messages.warning(request, 'Not Successful')
        return redirect('portal')
    return render(request, 'myapp/portal.html')


def purchase_item(request, pk):
    if request.method == 'POST':
        name = request.POST.get('purchaser')
        phone = request.POST.get('phone')
        # Get the product details from the database based on pk
        product = Product.objects.get(id=pk)

        user = product.owner.slug
        price = product.itemamount
        # Default to 1 if not provided
        quantity = request.POST.get('itemquantity', 1)
        size = request.POST.get('itemsize', '')
        color = request.POST.get('itemcolors', '')

        print(quantity, size, color, price)

        # Create a CartItem record with the user's information
        CartItem.objects.create(
            product=product,
            slug=user,
            purchaser=name,
            phone=phone,
            name=product.itemname,
            price=price,
            quantity=quantity,
            size=size,
            color=color,
            total_price=float(price) * int(quantity),
            cart_image=product.itemimage,  # You may need to adjust this field
            image_url=product.itemimage,
        )

        messages.success(
            request, 'Your order has been received. You will be contacted shortly. Thank You')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        HttpResponseRedirect(
            reverse('product', kwargs={'pk': product}))
    else:
        messages.warning(request, 'Invalid request.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# First General Search View
# def search(request, pk):
#     user = get_object_or_404(User, slug=pk)
#     shop = Product.objects.filter(owner=user)

#     q = request.GET.get('q') if request.GET.get('q') != None else ''

#     # product = Product.objects.filter(Q(itemcategory__icontains=q) |
#     #                                  Q(itemname__icontains=q) |
#     #                                  Q(itemamount__icontains=q) |
#     #                                  Q(itemcolors__icontains=q)

#     #                                  )
#     product = shop.filter(Q(itemcategory__icontains=q) |
#                           Q(itemname__icontains=q) |
#                           Q(itemamount__icontains=q) |
#                           Q(itemcolors__icontains=q)

#                           )

#     categories = product.values('itemcategory').distinct()

#     # shop = Product.objects.filter(owner=user)

#     # # Calculate discount price and percentage for each product in the shop
#     # for item in shop:
#     #     if item.itemdiscount:
#     #         discountprice = item.itemprice - item.itemdiscount
#     #         discountpercentage = int((
#     #             item.itemdiscount / item.itemprice) * 100)
#     #     else:
#     #         discountprice = None
#     #         discountpercentage = None

#     context = {'categories': categories, 'shop': shop, 'user': user,
#                #    'discountpercentage': discountpercentage, 'discountprice': discountprice
#                }
#     return render(request, 'shopapp/search.html', context)

# A nice one for exact
# def search(request, pk):
#     user = get_object_or_404(User, slug=pk)
#     shop = Product.objects.filter(owner=user)

#     q = request.GET.get('q', '')

#     # Filter numeric fields with exact match, and other fields with case-insensitive exact match
#     product = shop.filter(Q(itemcategory__iexact=q) |
#                           Q(itemname__iexact=q) |
#                           Q(itemcolors__iexact=q))

#     # Filter itemamount with exact match only if it's numeric
#     if q.isdigit():
#         product = product.filter(itemamount=q)

#     categories = product.values('itemcategory').distinct()

#     context = {'categories': categories, 'shop': product, 'user': user}

#     return render(request, 'shopapp/search.html', context)

# Nearly Perfect
# def search(request, pk):
#     user = get_object_or_404(User, slug=pk)
#     shop = Product.objects.filter(owner=user)

#     q = request.GET.get('q', '')

#     # Filter numeric fields with exact match, and other fields with case-insensitive exact match
#     product = shop.filter(Q(itemcategory__iexact=q) |
#                           Q(itemname__icontains=q) |
#                           Q(itemcolors__iexact=q))

#     # Filter itemamount with exact match only if it's numeric
#     if q.isdigit():
#         product = product.filter(itemamount=q)

#     categories = product.values('itemcategory').distinct()

#     context = {'categories': categories, 'shop': product, 'user': user}

#     return render(request, 'shopapp/search.html', context)

#
#

# PERFECT


def search(request, pk):
    user = get_object_or_404(User, slug=pk)
    shop = Product.objects.filter(owner=user)

    q = request.GET.get('q', '')

    # Filter for exact name match
    exact_name_match = shop.filter(itemname__iexact=q)

    # Filter for items containing the name
    contains_name = shop.annotate(full_name=Concat(
        'itemname', Value(' '))).filter(full_name__icontains=q)

    # Filter numeric fields with exact match, and other fields with case-insensitive exact match
    product = exact_name_match | contains_name

    # Filter itemamount with exact match only if it's numeric
    if q.isdigit():
        product = product.filter(itemamount=q)

    categories = product.values('itemcategory').distinct()

    context = {'categories': categories, 'shop': product, 'user': user}

    return render(request, 'shopapp/search.html', context)


# ----------Django Rest Framework For Product------------------
class ProductPostListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def delete(self, request, *args, **kwargs):
    #     User.objects.all().delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"


# ----------Django Rest Framework For CartItems------------------
class CartItemPostListCreate(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    # def delete(self, request, *args, **kwargs):
    #     User.objects.all().delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = "pk"
