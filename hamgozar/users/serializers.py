from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BaseUser, Profile
from .validators import number_validator, letter_validator, special_char_validator


class InputRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(max_length=20)
    bio = serializers.CharField(max_length=1000, required=False)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=10)
        ]
    )
    confirm_password = serializers.CharField(max_length=255)

    def validate_email(self, email):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email Already Taken")
        return email

    def validate_phone(self, phone):
        if BaseUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("phone number Already Taken")
        return phone

    def validate_username(self, username):
        if BaseUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("username Already Taken")
        return username

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("confirm password is not equal to password")
        return data


class OutPutRegisterSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = BaseUser
        fields = ("uuid", "first_name", "last_name", "email", "phone",
                  "username", "token", "created_at", "updated_at", "username")

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class OutPutProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("uuid", "bio", "posts_count", "subscriber_count",
                  "subscription_count", "avatar", "address")
