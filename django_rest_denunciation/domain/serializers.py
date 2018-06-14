from rest_framework import serializers
from denunciation.serializers import DenunciationSerializer
from .models import Domain, DomainAdministrator

class DomainAdministratorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DomainAdministrator
        fields = [
            'username',
            'password',
        ]


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Domain
        fields = '__all__'
