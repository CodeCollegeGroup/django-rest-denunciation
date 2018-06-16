from rest_framework import serializers
from .models import Domain, DomainAdministrator


class DomainAdministratorSerializer(serializers.HyperlinkedModelSerializer):

    domain_set = serializers.HyperlinkedRelatedField(
        view_name='domain-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = DomainAdministrator
        fields = [
            'username',
            'email',
            'password',
            'domain_set',
        ]


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Domain
        fields = '__all__'
