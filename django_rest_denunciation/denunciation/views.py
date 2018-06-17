from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_rest_denunciation.throttle import DenouncerRateThrottle
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
from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes
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

    throttle_classes = (DenouncerRateThrottle,)

    def post(self, request, format=None):
        denunciable, denunciation = self._get_splitted_data(request)
        saved_denunciable = self._save_serialized(
            denunciable, DenunciableSerializer, request
        )

        categories_data = denunciation['categories']
        categories_urls = self._get_categories_urls(categories_data, request)

        denunciable_url = self._get_denunciable_url(saved_denunciable, request)

        denunciation['categories'] = categories_urls
        denunciation['denunciable'] = denunciable_url

        self._save_serialized(denunciation, DenunciationSerializer, request)

        ok_status = {'ok': 'Complete denunciation saved successfully'}
        return Response(ok_status, status.HTTP_201_CREATED)

    @staticmethod
    def _save_serialized(data, serializer_class, request):
        serialized_data = serializer_class(
            data=data, context={'request': request}
        )

        serialized_data.is_valid(raise_exception=True)
        saved_serialized = serialized_data.save()

        return saved_serialized

    @staticmethod
    def _get_denunciable_url(denunciable, request):
        kwargs = {'pk': denunciable.pk}
        denunciable_url = reverse('denunciable-detail', kwargs=kwargs)
        denunciable_url = request.build_absolute_uri(denunciable_url)

        return denunciable_url

    @staticmethod
    def _get_categories_urls(categories, request):
        def get_categorie_url(category):
            pk = DenunciationCategory.objects.get(name=category).pk
            categorie_url = reverse('denunciationcategory-detail',
                                    kwargs={'pk': pk})
            categorie_url = request.build_absolute_uri(categorie_url)

            return categorie_url

        return [get_categorie_url(category) for category in categories]

    @staticmethod
    def _get_splitted_data(request):
        data = request.data.copy()

        try:
            denunciable = data['denunciable']
            denunciation = data['denunciation']
        except KeyError:
            raise ValidationError(
                "Sent dict must have 'denunciation' and 'denunciable' keys",
                code=status.HTTP_400_BAD_REQUEST
            )

        return denunciable, denunciation
