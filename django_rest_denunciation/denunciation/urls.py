from django.conf.urls import url
from rest_framework import routers
from .views import (
    DenunciationViewSet,
    DenunciableViewSet,
    DenunciationCategoryViewSet,
    DenunciationCompleteList
)

ROUTER = routers.DefaultRouter()
ROUTER.register(r'denunciation', DenunciationViewSet)
ROUTER.register(r'denunciable', DenunciableViewSet)
ROUTER.register(r'denunciation-category', DenunciationCategoryViewSet)

urlpatterns = ROUTER.urls  # pylint: disable=invalid-name

urlpatterns += [
    url(r'denunciation-complete', DenunciationCompleteList.as_view()),
]
