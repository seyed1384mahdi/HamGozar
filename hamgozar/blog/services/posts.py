from hamgozar.blog.models import Post, Subscription
from hamgozar.users.models import BaseUser, Profile

from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify
from django.core.cache import cache


def count_follower(*, user: BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()

def count_following(*, user: BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def count_posts(*, user: BaseUser) -> int:
    return Post.objects.filter(author=user).count()

def subscribe(*, user: BaseUser, username: str) -> Subscription:
    target = BaseUser.objects.get(username=username)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()

    return sub

def unsubscribe(*, user: BaseUser, username: str):
    target = BaseUser.objects.get(username=username)
    Subscription.objects.get(subscriber=user, target=target).delete()

@transaction.atomic
def create_post(*, user: BaseUser, title: str, content: str) -> Post:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )

    return post
