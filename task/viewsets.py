from rest_framework import viewsets, mixins, filters
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from . models import TaskList, Task, Attachment

from . permissions import IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone , IsAllowedToEditAttachmentElseNone

#def update_task_status(self, request, pk=None):
from rest_framework.decorators import action
from rest_framework import response
from . models import COMPLETE, NOT_COMPLETE
from django.utils import timezone
from rest_framework import status as s

from django_filters.rest_framework import DjangoFilterBackend
   
################################# TASKLIST VIEWSET ###########################################
""" OLD VERSION
class TaskListViewSet(viewsets.ModelViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
"""

#WHY WOULD I DO THIS WHEN ALL 5x functions() included as with ModelViewSet, NOOOO LIST is not there
class TaskListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                      mixins.DestroyModelMixin, viewsets.GenericViewSet): #mixins.ListModelMixin
    # Retrieve = GET (ID), Update (ID), Destroy (ID)
    # CREATE and LIST (POST, GET all)
    # Generic ViewSet needed for - GET OBJECT and GET QUERY_SET
    #MIXINS to limit the TASK LIST listed in view

    permission_classes = ( IsAllowedToEditTaskListElseNone ,)
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer

################################# TASK VIEWSET ###########################################
"""
#WAY 0 - NORMAL - can see all tasks if user AUTH and belongs to any house 
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAllowedToEditTaskElseNone, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
"""

"""
#WAY 1 - MIXIN - not see any LIST blocked
class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin, viewsets.GenericViewSet): #mixins.ListModelMixin
    permission_classes = (IsAllowedToEditTaskElseNone, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
"""

#WAY 2 - GET_QUERYSET() - to see only tasks created by me
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAllowedToEditTaskElseNone, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] #viewset needs to use djangofilterbackend
    filterset_fields = ['status' ,] #property expected on ViewSet
    search_fields = ['name', 'description',]
    #WORK WITHOUT COMMA

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset


    @action(detail=True, methods=['patch'])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            status = request.data['status']
            if (status == NOT_COMPLETE):
                if (task.status == COMPLETE):
                    task.status = NOT_COMPLETE
                    task.completed_on = None
                    task.completed_by = None
                else:
                    raise Exception("Task is already marked as not complete.")
            elif (status == COMPLETE):
                if (task.status == NOT_COMPLETE):
                    task.status = COMPLETE
                    task.completed_on = timezone.now()
                    task.completed_by = profile
                else:
                    raise Exception("Task already marked complete.")
            else:
                raise Exception("Incorrect status provided.")  #If you do not do C or NC, like AAAAA
            task.save()
            serializer = TaskSerializer(instance=task, context={'request': request})
            return response.Response(serializer.data, status=s.HTTP_200_OK)
        except Exception as e:
            return response.Response({'detail': str(e)}, status=s.HTTP_400_BAD_REQUEST)

################################# ATTACHMENT VIEWSET ###########################################
"""OLD VERSION
class AttachmentViewSet(viewsets.ModelViewSet): 
    # permission_classes = (IsAllowedToEditAttachmentElseNone ,)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
"""
#noone should see ATTACHMENT LIST (can POST but not SEE/LIST), see attachments via link provided on TASK list
class AttachmentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                      mixins.DestroyModelMixin,  viewsets.GenericViewSet): #mixins.ListModelMixin
    permission_classes = (IsAllowedToEditAttachmentElseNone ,)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    
    
