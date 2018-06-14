from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)
from .views import DomainViewSet, DomainAdministratorViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^domains', DomainViewSet)
ROUTER.register(r'^admins', DomainAdministratorViewSet)

urlpatterns = ROUTER.urls  # pylint: disable=invalid-name

urlpatterns += [
    url(r'authenticate/$', obtain_jwt_token),
    url(r'refresh/$', refresh_jwt_token),
]
