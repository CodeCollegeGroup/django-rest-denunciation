from rest_framework import serializers
from denunciation.serializers import DenunciationSerializer
from .models import Domain, DomainAdministrator


class DomainAdministratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainAdministrator
        fields = [
            'username',
            'password',
        ]


class DomainSerializer(serializers.ModelSerializer):

    denunciation_set = DenunciationSerializer(many=True)
    administrator = DomainAdministratorSerializer()

    class Meta:
        model = Domain
        fields = [
            'uri',
            'key',
            'denunciation_set',
            'administrator',
        ]
