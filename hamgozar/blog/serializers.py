from rest_framework import serializers

from django.urls import reverse

from .models import Subscription, Post


class InputSubscribeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class OutputSubscribeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Subscription
        fields = ('username', )

    def get_username(self, subscription):
        return getattr(subscription.target, subscription.target.USERNAME_FIELD)


class FilterSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=100)
    search = serializers.CharField(required=False, max_length=100)
    created_at__range = serializers.CharField(required=False, max_length=100)
    author__in = serializers.CharField(required=False, max_length=100)
    slug = serializers.CharField(required=False, max_length=100)
    content = serializers.CharField(required=False, max_length=100)


class InputPostSerializer(serializers.Serializer):
    content = serializers.CharField(required=False, max_length=100)
    title = serializers.CharField(required=False, max_length=100)


class OutputPostSerializer(serializers.Serializer):
    author = serializers.SerializerMethodField('get_author')
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Post
        fields = ('url', 'title', 'author')

    def get_author(self, obj):
        return obj.author.username

    def get_url(self, obj):
        request = self.context.get('request')
        path = reverse('api:blog:post_detail', args=(obj.slug,))
        return request.build_absolute_uri(path)

class OutputPostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Post
        fields = ('author', 'slug', 'title', 'content', 'created_at', 'updated_at')

    def get_author(self, obj):
        return obj.author.username