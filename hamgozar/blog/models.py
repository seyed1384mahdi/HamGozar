from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from hamgozar.common.models import BaseModel


User = get_user_model()


class Post(BaseModel):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=100, unique=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.slug


class Subscription(BaseModel):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='subscriptions')
    target = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='targets')

    class Meta:
        unique_together = ('subscriber', 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({'detail': 'You cannot subscribe yourself'})

    def __str__(self):
        return f'{self.subscriber.enail} - {self.target.email}'

