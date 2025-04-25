from django.db.models import QuerySet

from hamgozar.blog.models import Product


def get_products() -> QuerySet[Product]:
    return Product.objects.all()
