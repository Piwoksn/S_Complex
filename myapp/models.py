from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# To Delete Images
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# To Compress Image
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os


# # Create your models here.


class User(AbstractUser):

    profilepic = models.ImageField(null=True, blank=True, default="avatar.png")
    moredesc = models.TextField(null=True, blank=True)
    businessname = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    # businesstype = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    meansofid = models.CharField(max_length=100, null=True, blank=True)
    idnumber = models.CharField(max_length=100, null=True, blank=True)
    idpic = models.ImageField(null=True, blank=True)
    # shopcategory = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, default="icon.png")
    currency = models.CharField(max_length=10, null=True, blank=True)
    coins = models.IntegerField(blank=True, null=True, default=0)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    # dob = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    subscribed = models.BooleanField(default=False, null=True, blank=True)
    passwordresetcode = models.CharField(max_length=200, null=True, blank=True)
    passwordresetphone = models.CharField(
        max_length=200, null=True, blank=True)
    securityquestion = models.CharField(max_length=200, null=True, blank=True)
    securityanswer = models.CharField(max_length=100, null=True, blank=True)
    # FREE TRIAL
    date = models.DateTimeField(default=datetime.now())
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    record = models.FileField(upload_to="records/", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def compress_image(self, image, max_size=(800, 800), img_format='JPEG', quality=80):
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
        if self.pk is None:
            # Set the trial start date to the current date

            # ----Correct One------
            self.trial_start = self.date_joined
            self.trial_end = self.trial_start + \
                timedelta(days=14)  # Adjust trial period as needed

        else:
            self.trial_start = self.date_joined
            # Adjust the trial period as needed
            # self.trial_end = self.trial_start + timedelta(days=14)
            self.trial_end = self.trial_start + timedelta(days=14)

        # --------------------------------------------------------

            old_user = User.objects.get(pk=self.pk)
            if self.profilepic != old_user.profilepic:
                self.profilepic = self.compress_image(self.profilepic)
            if self.logo != old_user.logo:
                self.logo = self.compress_image(self.logo)

            # check old subscribers
            if old_user.subscribed != self.subscribed:
                if self.subscribed:
                    # User has subscribed
                    self.update_slug_activation()
                else:
                    # User has unsubscribed
                    self.slug = None

        # Update subscribed status before updating slug
        if self.trial_end <= timezone.now() and not self.subscribed:
            self.subscribed = False
        else:
            self.subscribed = True

        if self.subscribed:
            self.slug = slugify(self.businessname)
        else:
            self.slug = None

        super(User, self).save(*args, **kwargs)

    def update_slug_activation(self):
        if self.subscribed == False:
            self.slug = None
        elif self.trial_end <= self.date:
            self.slug = None
        else:
            # Reactivate the slug by generating a new one
            self.slug = slugify(self.businessname)


# @receiver(pre_save, sender=User)
# def delete_old_images(sender, instance, **kwargs):
#     if instance.pk:
#         old_item = User.objects.get(pk=instance.pk)
#         if old_item.profilepic != instance.profilepic:
#             old_item.profilepic.delete(save=False)
#         if old_item.logo != instance.logo:
#             old_item.logo.delete(save=False)

@receiver(pre_save, sender=User)
def delete_old_images(sender, instance, **kwargs):
    if instance.pk:
        old_item = User.objects.get(pk=instance.pk)
        if old_item.profilepic != instance.profilepic:
            # Check if the new profilepic is not the default image
            if str(instance.profilepic) != "avatar.png":
                old_item.profilepic.delete(save=False)
        if old_item.logo != instance.logo:
            # Check if the new logo is not the default image
            if str(instance.logo) != "icon.png":
                old_item.logo.delete(save=False)


@receiver(pre_delete, sender=User)
def delete_image(sender, instance, **kwargs):
    instance.profilepic.delete(save=False)


@receiver(pre_delete, sender=User)
def delete_logo(sender, instance, **kwargs):
    instance.logo.delete(save=False)


# -------------------------------COMMON.PY----------------------------------------------
