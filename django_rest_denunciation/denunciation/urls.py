from rest_framework import routers
from .views import DenunciationViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^denunciation_set', DenunciationViewSet)

urlpatterns = ROUTER.urls  # pylint: disable=invalid-name
