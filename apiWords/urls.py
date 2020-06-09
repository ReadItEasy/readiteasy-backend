from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers
from apiWords.views import MandarinWordSet


router = routers.DefaultRouter()
router.register(r'mandarin', MandarinWordSet)

urlpatterns = [
    url(r'^', include(router.urls)),

]