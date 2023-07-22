from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.serializers import OnlyHtmlSerializer


class OnlyHtmlViewSet(GenericAPIView):
    def get_serializer(self, *args, **kwargs):
        return OnlyHtmlSerializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response({'status': 'success'})
