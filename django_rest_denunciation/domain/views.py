from smtplib import SMTPException
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Domain, DomainAdministrator
from .serializers import DomainSerializer, DomainAdministratorSerializer


class DomainViewSet(viewsets.ModelViewSet):

    serializer_class = DomainSerializer
    queryset = Domain.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Create a domain generating a key and sending it to the domain admin
        """
        response = Response()
        data = request.data
        try:
            admin = DomainAdministrator.objects.get(
                pk=data.get('administrator')
            )
            domain = Domain.objects.create(
                application_name=data.get('application_name'),
                uri=data.get('uri'),
                administrator=admin,
            )
            message = """Olá, obrigado por registrar um
                         domínio em nossa plataforma\n
                         A chave do seu domínio '{}' é\n
                         Chave: {}""".format(domain.uri, domain.key)
            admin.send_email('Domínio registrado!', message)
        except ValidationError:
            response = Response(
                {'detail': 'error during creation of the domain'},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except ObjectDoesNotExist:
            response = Response(
                {'detail': 'user not found'},
                status.HTTP_404_NOT_FOUND
            )
        except SMTPException:
            response = Response(
                {'detail': 'error while sending email'},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class DomainAdministratorViewSet(viewsets.ModelViewSet):

    serializer_class = DomainAdministratorSerializer
    queryset = DomainAdministrator.objects.all()

    @action(methods=['put'], detail=False)
    def reset_password(self, request):
        """Reset password sending in e-mail"""

        response = Response()
        data = request.data
        try:
            user = DomainAdministrator.objects.get(
                email=data.get('email'),
            )
            user.recover_password()
        except ObjectDoesNotExist:
            response = Response(
                {'detail': 'user not found'},
                status.HTTP_404_NOT_FOUND
            )
        except SMTPException:
            response = Response(
                {'detail': 'error while sending email'},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response

    @action(methods=['get'], detail=False)
    def recover_domain_key(self, request):
        """Send Domain key to the domain administrator """

        response = Response()
        data = request.data
        try:
            domain = Domain.objects.get(
                application_name=data.get('application_name')
            )
            admin = domain.administrator
            message = """Olá,\nA chave do seu domínio '{}' é\n
                         Chave: {}""".format(domain.uri, domain.key)
            admin.send_email(
                'Equipe Django Rest Denunciation',
                message
            )
        except ObjectDoesNotExist:
            response = Response(
                {'detail': 'domain not found'},
                status.HTTP_404_NOT_FOUND
            )
        except SMTPException:
            response = Response(
                {'detail': 'error while sending email'},
                status.HTTP_500_INTERNAL_SERVER_ERROR
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
            response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
