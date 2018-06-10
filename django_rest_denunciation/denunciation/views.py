from rest_framework import viewsets
from .models import Denunciation
from .serializers import DenunciationSerializer


class DenunciationViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciationSerializer
    queryset = Denunciation.objects.all()
