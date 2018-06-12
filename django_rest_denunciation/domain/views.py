from smtplib import SMTPException
from json import dumps
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Domain, DomainAdministrator
from .serializers import DomainSerializer, DomainAdministratorSerializer


class DomainViewSet(viewsets.ModelViewSet):

    serializer_class = DomainSerializer
    queryset = Domain.objects.all()


class DomainAdministratorViewSet(viewsets.ModelViewSet):

    serializer_class = DomainAdministratorSerializer
    queryset = DomainAdministrator.objects.all()

    @action(methods=['put'], detail=True)
    def reset_password(self, request, pk=None):
        """Reset password sending in e-mail"""

        response = Response()
        data = request.data
        try:
            user = DomainAdministrator.objects.get(
                email=data.get('email'),
                pk=pk
            )
            user.recover_password()
        except ObjectDoesNotExist:
            response = Response(
                dumps({'detail': 'user not found'}),
                status=404
            )
        except SMTPException:
            response = Response(
                dumps({'detail': 'error while sending email'}),
                status=500
            )
        return response

    def create(self, request, *args, **kwargs):
        response = Response()
        data = request.data
        try:
            DomainAdministrator.objects.create_user(
                username=data.get('username'),
                password=data.get('password')
            )
        except ValidationError:
            response = Response(status=500)
        return response
