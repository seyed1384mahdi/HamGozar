from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

from hamgozar.api.mixins import ApiAuthMixin
from hamgozar.api.pagination import LimitOffsetPagination, get_paginated_response
from hamgozar.blog.models import Subscription
from hamgozar.blog.selectors.posts import get_subscribers
from hamgozar.blog.serializers import OutputSubscribeSerializer, InputSubscribeSerializer
from hamgozar.blog.services.posts import unsubscribe, subscribe


class SubscribeDetailApi(ApiAuthMixin, APIView):
    def delete(self, request, username):
        try:
            unsubscribe(user=request.user, username=username)
        except Exception as e:
            return Response(
                {'detail': 'Database Error - ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(responses=OutputSubscribeSerializer)
    def get(self, request):
        user = request.user
        query = get_subscribers(user=user)
        return get_paginated_response(
            request=request,
            pagination_class=self.Pagination,
            queryset=query,
            serializer_class=OutputSubscribeSerializer,
            view=self,
        )

    @extend_schema(
        request=InputSubscribeSerializer,
        responses=OutputSubscribeSerializer
    )
    def post(self, request):
        serializer = InputSubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = subscribe(user=request.user, username=serializer.data.get('username'))
        except Exception as e:
            return Response(
                {'detail': 'Database Error - ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        output_serializer = OutputSubscribeSerializer(query)
        return Response(output_serializer.data)
