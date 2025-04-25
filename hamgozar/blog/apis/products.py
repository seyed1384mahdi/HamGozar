from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_spectacular.utils import extend_schema

from hamgozar.api.pagination import LimitOffsetPagination
from hamgozar.blog.models import Product
from hamgozar.blog.services.products import create_product
from hamgozar.blog.selectors.products import get_products


class ProductApi(APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 20

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_product(name=serializer.validated_data.get('name'))
            return Response(self.OutputSerializer(query, context={"request": request}).data)
        except Exception as ex: # todo: fix this error swallowing
            return Response({'detail': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = get_products()
        return Response(self.OutputSerializer(query, context={"request": request}, many=True).data)
