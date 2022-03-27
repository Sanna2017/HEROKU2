from django.urls import path, include
from rest_framework import routers
from . viewsets import UserViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)


urlpatterns = [
    path ('',include(router.urls)),
]