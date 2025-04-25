from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InputRegisterSerializer, OutPutRegisterSerializer, OutPutProfileSerializer
from ..api.mixins import ApiAuthMixin
from .selectors import get_profile
from .services import register

from drf_spectacular.utils import extend_schema


class ProfileApi(ApiAuthMixin, APIView):
    @extend_schema(responses=OutPutProfileSerializer)
    def get(self, request):
        profile = get_profile(user=request.user)
        return Response(OutPutProfileSerializer(profile, context={"request":request}).data)


class RegisterApi(APIView):
    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(first_name=serializer.validated_data.get("first_name"), last_name=serializer.validated_data.get("last_name"),
                            email=serializer.validated_data.get("email"), password=serializer.validated_data.get("password"),
                            bio=serializer.validated_data.get("bio"), phone=serializer.validated_data.get("phone"),
                            address=serializer.validated_data.get("address"), username=serializer.validated_data.get("username"),
                            )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(OutPutRegisterSerializer(user, context={"request":request}).data)
