from rest_framework import serializers
from .models import Denunciation


class DenunciationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Denunciation
        fields = [
            'domain',
            'justification',
        ]
