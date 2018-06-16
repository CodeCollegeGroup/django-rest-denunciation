from rest_framework import (
    viewsets,
    generics,
    views,
    response,
    status
)
from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
)
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes
)
from rest_framework.permissions import AllowAny
from django_rest_denunciation.throttle import DenouncerThrottle


class UnauthenticateView(APIView):

    @api_view(['GET'])
    @permission_classes((AllowAny,))
    @throttle_classes([AnonRateThrottle,])
    def get(request, denouncer=None):
        content = {
            'status': 'request was permitted'
        }
        return response.Response(
            content,
            status=status.HTTP_200_OK
        )


class AuthenticateView(APIView):

    @api_view(['GET'])
    @throttle_classes([UserRateThrottle,])
    def get(request):
        content = {
            'status': 'request was permitted'
        }
        return response.Response(
            content,
            status=status.HTTP_200_OK
        )


class LimitUserView(APIView):

    @api_view(['POST'])
    @permission_classes((AllowAny,))
    @throttle_classes([DenouncerThrottle,])
    def get(request):

        content = {
            'status': 'request was permitted',
        }

        return response.Response(
            content,
            status=status.HTTP_200_OK
        )
