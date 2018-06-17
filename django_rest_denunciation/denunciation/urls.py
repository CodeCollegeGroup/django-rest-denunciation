from django.conf.urls import url
from denunciation.views import DenunciationList, DenunciationDetails
from rest_framework import routers
from .views import (
    DenunciableViewSet,
    DenunciationCategoryViewSet,
    DenouncerViewSet,
    change_denunciation_state
)

ROUTER = routers.DefaultRouter()
ROUTER.register(r'denunciable', DenunciableViewSet)
ROUTER.register(r'denunciation-category', DenunciationCategoryViewSet)
ROUTER.register(r'denouncer', DenouncerViewSet)

urlpatterns = ROUTER.urls

urlpatterns += [
    url(
        r'denunciation/$',
        DenunciationList.as_view(),
        name='denunciation-list'
    ),
    url(
        r'denunciation/(?P<pk>[0-9]+)/$',
        DenunciationDetails.as_view(),
        name='denunciation-detail'
    ),
    url(
        r'denunciation/(?P<pk>[0-9]+)/(?P<name>[a-z]+)/$',
        change_denunciation_state
    )
]
