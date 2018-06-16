from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
from denunciation.views import (
    AuthenticateView,
    UnauthenticateView,
    LimitUserView,
)

urlpatterns = [
    url(r'^unauthenticate/', UnauthenticateView.get),
    url(r'^authenticate/', AuthenticateView.get),
    url(r'^limit_user/(?P<denouncer>[a-z]+)/$', LimitUserView.get),
]
