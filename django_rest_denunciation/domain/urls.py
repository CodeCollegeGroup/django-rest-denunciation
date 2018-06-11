from rest_framework import routers
from .views import DomainViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^domains', DomainViewSet)

urlpatterns = ROUTER.urls
