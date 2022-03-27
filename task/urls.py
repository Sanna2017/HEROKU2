from django.urls import path, include
from rest_framework import routers 
from . viewsets import TaskListViewSet ,TaskViewSet, AttachmentViewSet

router = routers.DefaultRouter()
router.register ('tasklists', TaskListViewSet)
router.register ('tasks', TaskViewSet)
router.register ('attachments', AttachmentViewSet)

urlpatterns = [
    path ('',include(router.urls)),
]
