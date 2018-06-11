from rest_framework import viewsets
from .models import Domain
from .serializers import DomainSerializer


class DomainViewSet(viewsets.ModelViewSet):

    serializer_class = DomainSerializer
    queryset = Domain.objects.all()
