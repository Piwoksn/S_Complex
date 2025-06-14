from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('', include('shopapp.urls')),
    path('', include('subscription.urls')),
    path('', include('chats.urls')),
    path('api/', include('api.urls')),
    # 3rd Party 
    path('api/auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    
    
]

# Serve media files during development
# remove if settings.Debug
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
