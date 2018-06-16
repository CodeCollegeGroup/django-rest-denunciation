from rest_framework import serializers
from .models import (
    Denunciation,
    Denunciable,
    DenunciationCategory,
)


class DenunciableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denunciable
        fields = '__all__'


class DenunciationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denunciation
        fields = '__all__' 
        read_only_fields = ('current_state',)


class DenunciationCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DenunciationCategory
        fields = '__all__'


class DenunciationCompleteSerializer(serializers.Serializer):

    denunciation = DenunciationSerializer()

    denunciable = DenunciableSerializer()
