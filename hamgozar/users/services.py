from django.db import transaction 
from .models import BaseUser, Profile


def create_profile(*, user:BaseUser, bio:str | None, address: str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio, address=address)

def create_user(*, email:str, password:str, first_name: str,
                last_name: str, phone: str, username:str) -> BaseUser:

    return BaseUser.objects.create_user(email=email, password=password, first_name=first_name,
                                        last_name=last_name, phone=phone, username=username)


@transaction.atomic
def register(*, first_name: str, last_name: str, phone: str, address: str|None,
             bio:str|None, email:str, password:str, username: str) -> BaseUser:

    user = create_user(email=email, password=password, first_name=first_name,
                       last_name=last_name, phone=phone, username=username)

    create_profile(user=user, bio=bio, address=address)

    return user
