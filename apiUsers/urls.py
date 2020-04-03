from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf.urls import url, include
from rest_framework import routers
from apiUsers.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)




urlpatterns = [
    url(r'^', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]