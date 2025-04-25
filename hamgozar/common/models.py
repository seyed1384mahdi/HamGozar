from django.db import models
from django.utils import timezone

import uuid

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(default=None, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, db_index=True)

    class Meta:
        abstract = True
