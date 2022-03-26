from rest_framework import routers 
from . viewsets import HouseViewSet

router = routers.DefaultRouter()
router.register ('houses', HouseViewSet)



