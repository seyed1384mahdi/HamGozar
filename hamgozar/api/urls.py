from django.urls import path, include

urlpatterns = [
    path('blog/', include('hamgozar.blog.urls', namespace='blog'))
]
