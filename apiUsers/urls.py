from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .my_custom_jwt import MyTokenObtainPairView
from django.conf.urls import url, include
from rest_framework import routers
from apiUsers.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello'),

    url(r'^', include(router.urls)),

]