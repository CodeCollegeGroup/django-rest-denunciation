from json import loads
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework import serializers
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
    DenunciationCategorySerializer
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


class DenunciationComplete:

        def validate_data(self, data):
            denunciation = data.get('denunciation', None)
            denunciable = data.get('denunciable', None)

            error_response = None
            if denunciation is None or denunciable is None: 
                error_message = 'Please, send one key with denunciation and other with denunciable'
                error_response = {'detail': error_message}
           
            serialized_data = DenunciationSerializer(data=denunciation)
            error_response = (self._validate_serialized_data(serialized_data)
                              if error_response is None else error_response)

            serialized_data = DenunciableSerializer(data=denunciable)
            error_response = (self._validate_serialized_data(serialized_data)
                              if error_response is None else error_response)

            return error_response

        @staticmethod
        def _validate_serialized_data(serialized_data):
            try:
                serialized_data.is_valid(raise_exception=True)
            except serializers.ValidationError:
                return serialized_data.errors

            return None


class DenunciationCompleteList(APIView, DenunciationComplete):

    def post(self, request, format=None):
        data = request.data.dict()
        errors = self.validate_data(data)

        if not errors:
            serialized_data_denunciation = DenunciationSerializer(data=denunciation)

            serialized_data_denunciable = DenunciableSerializer(data=denunciable)
            denunciable = serialized_data_denunciable.save()

            denunciable_url = reverse(
                'denunciable-detail',
                kwargs={'pk': denunciable.pk}
            )

            denunciation['denunciable'] = denunciable_url
            serialized_data_denunciation.save()

            return Response(
                {'ok': 'Complete denunciation saved successfully'},
                status.HTTP_200_OK 
            )

        return Response({'errors': errors}, status.HTTP_400_BAD_REQUEST)
