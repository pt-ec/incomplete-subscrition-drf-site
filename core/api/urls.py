from django.urls import path, include

urlpatterns = [
    path('shop/', include('shop.api.urls')),

    path('subscription/',
         include('subscription.api.urls')),

    path('blog/', include('blog.api.urls')),

    path('dj-rest-auth/',
         include('dj_rest_auth.urls')),

    path('dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),
]
