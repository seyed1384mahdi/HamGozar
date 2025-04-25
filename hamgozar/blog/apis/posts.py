from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from hamgozar.api.mixins import ApiAuthMixin
from hamgozar.api.pagination import LimitOffsetPagination, get_paginated_response_context
from hamgozar.blog.selectors.posts import post_list, post_detail
from hamgozar.blog.serializers import InputPostSerializer, OutputPostSerializer, FilterSerializer, \
    OutputPostDetailSerializer
from hamgozar.blog.services.posts import create_post


class PostApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        request=InputPostSerializer,
        responses=OutputPostSerializer
    )
    def post(self, request):
        serializer = InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_post(
                user=request.user,
                content=serializer.validated_data.get('content'),
                title=serializer.validated_data.get('title'),
            )
        except Exception as e:
            return Response(
                {'detail': 'Database Error - ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(OutputPostSerializer(query, context={'request': request}).data)

    @extend_schema(
        parameters=[FilterSerializer],
        responses=OutputPostSerializer
    )
    def get(self, request):
        filter_serializer = FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        try:
            query = post_list(filters=filter_serializer.validated_data, user=request.user)
        except Exception as e:
            return Response(
                {'detail': 'Database Error - ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=OutputPostSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class PostDetailApi(ApiAuthMixin, APIView):
    @extend_schema(
        responses=OutputPostDetailSerializer,
    )
    def get(self, request, slug):
        try:
            query = post_detail(slug=slug, user=request.user)
        except Exception as e:
            return Response(
                {'detail': 'Database Error - ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = OutputPostDetailSerializer(query)

        return Response(serializer.data)
