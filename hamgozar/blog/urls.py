from django.urls import path

from hamgozar.blog.apis.products import ProductApi

app_name = 'blog'

urlpatterns = [
    path('product/', ProductApi.as_view(), name='product'),
]