from django.db import models

from hamgozar.common.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
