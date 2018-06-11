from rest_framework import routers
from .views import DomainViewSet, DomainAdministratorViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^domains', DomainViewSet)
ROUTER.register(r'^admins', DomainAdministratorViewSet)

urlpatterns = ROUTER.urls
