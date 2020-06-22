from django.urls import path, include

urlpatterns = [
    path('shop/', include('products.api.urls')),

    path('shop/', include('orders.api.urls')),

    path('subscription/',
         include('subscription_classes.api.urls')),

    path('subscription/kits/',
         include('subscription_kits.api.urls')),

    path('blog/', include('blog.api.urls')),

    path('dj-rest-auth/',
         include('dj_rest_auth.urls')),

    path('dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),
]
