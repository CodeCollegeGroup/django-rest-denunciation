from rest_framework import serializers
from .models import (
    Denunciable,
    DenunciationCategory,
    Denouncer,
    Denunciation
)


class DenunciationCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DenunciationCategory
        fields = '__all__'


class DenunciableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denunciable
        fields = '__all__'


class DenouncerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denouncer
        fields = '__all__'


class DenunciationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denunciation
        fields = '__all__'
