from json import loads
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Denunciation,
    Denunciable,
    DenunciationCategory
)
from .serializers import (
    DenunciationSerializer,
    DenunciableSerializer,
    DenunciationCategorySerializer,
    DenunciationCompleteSerializer
)


class DenunciationViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciationSerializer
    queryset = Denunciation.objects.all()


class DenunciableViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciableSerializer
    queryset = Denunciable.objects.all()


class DenunciationCategoryViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciationCategorySerializer
    queryset = DenunciationCategory.objects.all()


class DenunciationCompleteList(APIView):

    def post(self, request, format=None):
        try:
            data = request.data.copy()
            denunciable = data['denunciable']
            denunciation = data['denunciation']
        except:
            message = "Your dict must have 'denunciation' and 'denunciable'"
            return Response({'errors': message}, status.HTTP_400_BAD_REQUEST) 

        try:
            denunciable_serialized = DenunciableSerializer(
                data=denunciable,
                context={'request': request}
            )
            denunciable_serialized.is_valid(raise_exception=True)
            saved_denunciable = denunciable_serialized.save()
        except serializers.ValidationError:
            return Response(
                {'denunciable': denunciable_serialized.errors},
                status.HTTP_400_BAD_REQUEST
            )

        categories_urls = self._get_categories_urls(
            denunciation['categories'],
            request
        )
        denunciation['categories'] = categories_urls

        try:
            denunciation_serialized = DenunciationSerializer(
                data=denunciation, context={'request': request}
            )

            kwargs = {'pk': saved_denunciable.pk}
            denunciable_url = reverse('denunciable-detail', kwargs=kwargs)
            denunciable_url = request.build_absolute_uri(denunciable_url)
            denunciation['denunciable'] = denunciable_url

            denunciation_serialized.is_valid(raise_exception=True)
            denunciable_serialized.save()
        except serializers.ValidationError:
            return Response(
                {'denunciation': denunciation_serialized.errors},
                status.HTTP_400_BAD_REQUEST
            )

        ok_status = {'ok': 'Complete denunciation saved successfully'}
        return Response(ok_status, status.HTTP_201_CREATED)

    @staticmethod
    def _get_categories_urls(categories, request):
        def get_categorie_url(category):
            pk = DenunciationCategory.objects.get(name=category).pk
            categorie_url = reverse('denunciationcategory-detail',
                                    kwargs={'pk': pk})
            categorie_url = request.build_absolute_uri(categorie_url)

            return categorie_url

        return [get_categorie_url(category) for category in categories] 
