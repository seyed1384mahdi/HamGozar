from django.urls import path, include

urlpatterns = [
    path('blog/', include('hamgozar.blog.urls', namespace='blog')),
    path('users/', include('hamgozar.users.urls', namespace='users')),
    path('auth/', include('hamgozar.authentication.urls', namespace='authentication')),
]
