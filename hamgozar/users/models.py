from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from hamgozar.common.models import BaseModel

import uuid
import os


def _get_avatar_upload_path(obj, filename):
    now = timezone.now()
    base_path = "avatars"
    new_filename = str(uuid.uuid5(uuid.NAMESPACE_URL, obj.pk))
    ext = os.path.split(filename)[-1]
    p = os.path.join(base_path, now.strftime("%Y/%m"), f"{new_filename}{ext}")

    return p


class BaseUserManager(BUM):
    def create_user(self, email, first_name, last_name, phone, username, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin,
                          first_name=first_name, last_name=last_name, phone=phone, username=username)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, username, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            username=username
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField("First Name", max_length=150, blank=False)
    last_name = models.CharField("Last Name", max_length=150, blank=False)
    phone = models.CharField("Phone Number", max_length=20, blank=False, unique=True)
    email = models.EmailField("Email Address", unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_admin


class Profile(BaseModel):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="profile")
    posts_count = models.PositiveIntegerField(default=0)
    subscriber_count = models.PositiveIntegerField(default=0)
    subscription_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    address = models.TextField("Address", max_length=300, blank=True, null=True)
    avatar = models.ImageField(upload_to=_get_avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user} >> {self.bio}"
