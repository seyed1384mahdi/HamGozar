from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        self._add_ip_to_token(refresh)

        user_data = self._get_user_data()

        user_data['token'] = {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token)
        }

        return {**data, **user_data}

    def _add_ip_to_token(self, token):
        request = self.context.get('request')
        if request:
            ip_address = request.META.get('REMOTE_ADDR')
            token['ip'] = ip_address

    def _get_user_data(self):
        user = self.user
        data = {
            'uuid': user.uuid,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'username': user.username,
        }
        return data