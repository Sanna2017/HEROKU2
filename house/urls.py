from django.urls import path, include
from rest_framework import routers 
from . viewsets import HouseViewSet

router = routers.DefaultRouter()
router.register ('houses', HouseViewSet)


urlpatterns = [
    path ('',include(router.urls)),
]