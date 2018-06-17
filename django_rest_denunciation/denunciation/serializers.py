from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
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

    gravity_map = {
        '2': 'High',
        '1': 'Medium',
        '0': 'Low'
    }

    class Meta:
        model = DenunciationCategory
        fields = '__all__'

    def to_representation(self, instance):
        field_view = super().to_representation(instance)
        gravity = field_view['gravity']

        if gravity in ('0', '1', '2'):
            field_view['gravity'] = self.gravity_map[gravity]

        return field_view


class DenunciationQueueSerializer(serializers.Serializer):

    denunciation_queue = serializers.HyperlinkedRelatedField(
        view_name='denunciation-detail',
        many=True,
        read_only=True
    )
