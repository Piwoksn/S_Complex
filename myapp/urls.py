from django.urls import path
from . import views
# password reset
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('fgt_pwd', views.fgt_pwd, name='fgt_pwd'),
#     path('loginform', views.loginform, name='loginform'),
    path('more_info', views.more_info, name='more_info'),
    path('portal', views.portal, name='portal'),
    path('profile', views.profile, name='profile'),
#     path('registerform', views.registerform, name='registerform'),
    path('category', views.category, name='category'),
    path('item/<path:selected_category>/', views.item, name='item'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('order/<str:pk>/', views.order, name='order'),
    path('clear/<str:pk>/', views.clear, name='clear'),
    path('changepassword/<str:pk>/', views.changepassword, name='changepassword'),
    path('securityquestion/<str:pk>/',
         views.securityquestion, name='securityquestion'),
    path('confirmnumber/<str:pk>/',
         views.confirmnumber, name='confirmnumber'),
    path('superadmin', views.superadmin, name="superadmin"),
    path('superadminsearch', views.superadminsearch, name="superadminsearch"),
    path('superadminsubscription', views.superadminsubscription,
         name="superadminsubscription"),
    path('superadmincancelsub', views.superadmincancelsub,
         name="superadmincancelsub"),
    path('superadmincoin', views.superadmincoin,
         name="superadmincoin"),
    path('superadmindelete/<str:pk>/',
         views.superadmindelete, name="superadmindelete"),
    path('superadminlogin/',
         views.superadminlogin, name="superadminlogin"),
    path('superadminlogout/',
         views.superadminlogout, name="superadminlogout"),

    path('superadminedit/<str:pk>/',
         views.superadminedit, name="superadminedit"),

    path('info/', views.info, name="info"),

    # PAYSTACK and PAYPAL
    path('flutterwave-callback/', views.flutterwave_callback,
         name='flutterwave_callback'),
    path('paystack-callback/', views.paystack_callback, name='paystack_callback'),
    path('paypal/callback/', views.paypal_callback, name='paypal_callback'),
    # -------------------------------------
    # Functions
    path('process_data', views.process_data, name='process_data'),
    path('logout', views.logoutbutton, name='logout'),
    path('editproduct/<str:pk>/', views.editproduct, name='editproduct'),

    path('coins/', views.coins, name='coins'),
    path('submethod/', views.submethod, name='submethod'),
    path('coinsub/', views.coinsub, name='coinsub'),
    path('coincallback/', views.coincallback, name='coincallback'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('aboutus/', views.aboutus, name='aboutus'),

    path('purchaser/<str:pk>/<str:pk2>/', views.purchaser, name='purchaser'),
    path('search/<slug:pk>', views.cat_search, name="cat_search"),
    # ----------Django Rest Framework------------------
    path('user/', views.UserPostListCreate.as_view(), name="user"),
    path('user/<int:pk>', views.UserRetrieveUpdateDestroy.as_view(), name="update"),
    #     ------------End REst Framework-----


    path('refund_policy', views.refund_policy, name="refund_policy"),

]
