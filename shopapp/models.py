from django.db import models
from myapp.models import User

# To Delete Images
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# Compress Image
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
# Unique image
import uuid
from django.contrib.sessions.models import Session


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    itemcategory = models.CharField(max_length=200, null=True, blank=True)
    itemname = models.CharField(max_length=200, null=True, blank=True)
    itemimage = models.ImageField(upload_to="media/", blank=True, null=True)
    itemimage2 = models.ImageField(upload_to="media/", blank=True, null=True)
    itemimage3 = models.ImageField(upload_to="media/", blank=True, null=True)
    itemvideo = models.FileField(upload_to="media/", blank=True, null=True)
    itemprice = models.FloatField(null=True, blank=True)
    itemdiscount = models.FloatField(default=0, null=True, blank=True)
    itemamount = models.FloatField(null=True, blank=True)
    itemsize = models.CharField(max_length=200, blank=True, null=True)
    itemcolors = models.CharField(max_length=100, null=True, blank=True)
    itemdescription = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    paid = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.owner.email

    # def compress_image(self, image, max_size=(800, 800), img_format='JPEG', quality=80):
    def compress_image(self, image, max_size=(800, 800), img_format='JPEG', quality=95):
        try:
            # Open the image using Pillow (PIL)
            img = Image.open(image)

            # Resize the image to the maximum size
            img.thumbnail(max_size)

            # Create an in-memory buffer to save the compressed image
            buffer = BytesIO()
            img.save(buffer, format=img_format, quality=quality)
            buffer.seek(0)

            return ContentFile(buffer.read(), name=image.name)
        except:
            return image  # Return the original image if there is an issue

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_user = Product.objects.get(pk=self.pk)
            if self.itemimage != old_user.itemimage:
                self.itemimage = self.compress_image(
                    self.itemimage, quality=95)

            if self.itemimage2 != old_user.itemimage2:
                self.itemimage2 = self.compress_image(
                    self.itemimage2, quality=95)

            if self.itemimage3 != old_user.itemimage3:
                self.itemimage3 = self.compress_image(
                    self.itemimage3, quality=95)

        super(Product, self).save(*args, **kwargs)


@receiver(pre_save, sender=Product)
def delete_old_images(sender, instance, **kwargs):
    if instance.pk:
        old_item = Product.objects.get(pk=instance.pk)
        if old_item.itemimage != instance.itemimage:
            old_item.itemimage.delete(save=False)

        if old_item.itemimage2 != instance.itemimage2:
            old_item.itemimage2.delete(save=False)

        if old_item.itemimage3 != instance.itemimage3:
            old_item.itemimage3.delete(save=False)

        if old_item.itemvideo != instance.itemvideo:
            old_item.itemvideo.delete(save=False)


@receiver(pre_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    instance.itemimage.delete(save=False)
    instance.itemimage2.delete(save=False)
    instance.itemimage3.delete(save=False)
    instance.itemvideo.delete(save=False)


# ____________________________________


# ____________________________________
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)

    slug = models.SlugField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    purchaser = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_purchased = models.BooleanField(default=False, null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    cart_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.name} ({self.product.owner.email})"
