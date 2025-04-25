from hamgozar.blog.models import Product


def create_product(name: str) -> Product:
    product = Product.objects.create(name=name)
    product.full_clean()
    product.save()
    return product


