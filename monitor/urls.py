from django.conf.urls import patterns, include, url

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'result', views.ResultViewSet)

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
)