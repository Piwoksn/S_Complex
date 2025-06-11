from django.db import models
from myapp.models import User
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.owner.email if self.owner else "Unknown Owner"

    def compress_image(self, image, max_size=(800, 800), img_format='JPEG', quality=95):
        try:
            img = Image.open(image)
            img.thumbnail(max_size)
            buffer = BytesIO()
            img.save(buffer, format=img_format, quality=quality)
            buffer.seek(0)
            return ContentFile(buffer.read(), name=image.name)
        except Exception as e:
            return image

    def save(self, *args, **kwargs):
        # Only compress if updating an existing instance
        if self.pk and Product.objects.filter(pk=self.pk).exists():
            old = Product.objects.get(pk=self.pk)

            if self.itemimage and self.itemimage != old.itemimage:
                self.itemimage = self.compress_image(self.itemimage)

            if self.itemimage2 and self.itemimage2 != old.itemimage2:
                self.itemimage2 = self.compress_image(self.itemimage2)

            if self.itemimage3 and self.itemimage3 != old.itemimage3:
                self.itemimage3 = self.compress_image(self.itemimage3)

        else:
            # New object – compress if images exist
            if self.itemimage:
                self.itemimage = self.compress_image(self.itemimage)

            if self.itemimage2:
                self.itemimage2 = self.compress_image(self.itemimage2)

            if self.itemimage3:
                self.itemimage3 = self.compress_image(self.itemimage3)

        super().save(*args, **kwargs)


@receiver(pre_save, sender=Product)
def delete_old_images(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        return

    # Compare and delete only if changed
    for field in ['itemimage', 'itemimage2', 'itemimage3', 'itemvideo']:
        old_file = getattr(old, field)
        new_file = getattr(instance, field)
        if old_file and old_file != new_file:
            old_file.delete(save=False)


@receiver(pre_delete, sender=Product)
def delete_images_on_delete(sender, instance, **kwargs):
    for field in ['itemimage', 'itemimage2', 'itemimage3', 'itemvideo']:
        file = getattr(instance, field)
        if file:
            file.delete(save=False)


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cart_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        product_owner = self.product.owner.email if self.product and self.product.owner else "Unknown"
        return f"{self.quantity} x {self.name} ({product_owner})"
