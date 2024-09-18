from django.urls import path
from . import views


urlpatterns = [
    path('createchats', views.createchat, name='createchats'),
    path('superadminmessages', views.superadminmessages, name='superadminmessages'),
    path('adminchats/<str:email>', views.superadminchatroom, name='adminchats'),
    path('adminchatdelete/<str:email>',
         views.superadminchatdelete, name='adminchatdelete'),

    path('userchat/<str:email>', views.userchat, name="userchat"),
]
