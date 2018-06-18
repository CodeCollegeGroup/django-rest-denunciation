from rest_framework import serializers
from .models import (
    Denunciable,
    DenunciationCategory,
    Denouncer,
    Denunciation,
    DenunciationState
)


class DenunciationCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DenunciationCategory
        fields = '__all__'


class DenunciableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denunciable
        fields = '__all__'
        read_only_fields = ('gravity',)


class GravitedSerializer(serializers.HyperlinkedModelSerializer):

    gravity_map_to_str = {
        2: 'High',
        1: 'Medium',
        0: 'Low'
    }

    gravity_map_to_int = dict((v, k) for k, v in gravity_map_to_str.items())

    def is_valid(self, raise_exception=False):
        gravity = self.initial_data.get('gravity', None)

        if gravity in ('High', 'Medium', 'Low'):
            self.initial_data['gravity'] = self.gravity_map_to_int[gravity]

        super(GravitedSerializer, self).is_valid(
            raise_exception=raise_exception
        )

    def to_representation(self, instance):
        field_view = super().to_representation(instance)
        gravity = field_view['gravity']

        if gravity in (0, 1, 2):
            field_view['gravity'] = self.gravity_map_to_str[gravity]

        return field_view


class DenunciationSerializer(GravitedSerializer):

    class Meta:
        model = Denouncer
        fields = '__all__'
        read_only_fields = ('current_state', 'gravity')


class DenunciationCategorySerializer(GravitedSerializer):

    class Meta:
        model = Denunciation
        fields = '__all__'


class DenunciationQueueSerializer(serializers.Serializer):
    # pylint: disable=abstract-method

    denunciation_queue = serializers.HyperlinkedRelatedField(
        view_name='denunciation-detail',
        many=True,
        read_only=True
    )


class DenunciationStateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DenunciationState
        fields = '__all__'

class DenouncerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Denouncer
        fields = '__all__'
