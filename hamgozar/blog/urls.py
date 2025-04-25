from django.urls import path

from .apis.posts import PostApi, PostDetailApi
from .apis.subs import SubscribeApi, SubscribeDetailApi


app_name = "blog"
urlpatterns = [
        path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
        path("subscribe/<str:username>", SubscribeDetailApi.as_view(), name="subscribe_detail"),
        path("post/", PostApi.as_view(), name="post"),
        path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail"),
        ]