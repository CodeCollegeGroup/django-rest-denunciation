from rest_framework import serializers
from .models import Domain
from denunciation.serializers import DenunciationSerializer


class DomainSerializer(serializers.ModelSerializer):

    denunciation_set = DenunciationSerializer(many=True)

    class Meta:
        model = Domain
        fields = [
            'uri',
            'key',
            'denunciation_set',
        ]
