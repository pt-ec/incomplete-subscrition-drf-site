from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shop/', include('products.api.urls')),
    path('api/v1/shop/', include('orders.api.urls')),
    path('api/v1/subscription/kits/',
         include('subscription_kits.api.urls')),
    path('api/v1/subscription/classes/',
         include('subscription_classes.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/',
         include('dj_rest_auth.registration.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
