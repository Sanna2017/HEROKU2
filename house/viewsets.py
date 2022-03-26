from rest_framework import viewsets, filters
from .serializers import HouseSerializer
from . models import House

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from . permissions import IsHouseManagerOrNone

from rest_framework.permissions import IsAuthenticated 

from django_filters.rest_framework import DjangoFilterBackend

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsHouseManagerOrNone ,)    
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields = ['members' ,]
    search_fields = ['name', 'description',]
    #search_fields = ['=name', 'description',] # name RedStar exact, not only Red
    ordering_fields = ['points', 'completed_tasks_conut', 'notcompleted_tasks_count']
    

    #to add fun() to API, we need action DECORATOR
    @action(detail=True, methods=['post'], name='Join',permission_classes=(IsAuthenticated ,)) #, permission_classes=()
    # detail=True means that fun() is going to be applied on INSTANCE of model (not LIST of objects) 
    # method POST allowed with this specific action     
    def join(self, request, pk=None): # function() will allow user to join house
        # PK for model instance that this specific function gets called on
        try:
            house = self.get_object() #get obj this action was called upon
            user_profile = request.user.profile #we need to add house to user_profile
            if (user_profile.house == None): #does profile of current user have house?
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif (user_profile in house.members.all()): 
                return Response({'detail': 'Already a member in this house.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Already a member in another house.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['post'], name='Leave',permission_classes=(IsAuthenticated ,)) #, permission_classes=()
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if (user_profile in house.members.all()): #if user member in this house
                user_profile.house = None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'User not a member in this house.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['post'], name='Remove Member')
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get('user_id', None) #user which needs to be reomoved
            #but we do not have space to get it from somewhere, use POSTMAN
            if (user_id == None):
                return Response({'user_id': 'Not provided.'}, status=status.HTTP_400_BAD_REQUEST)
            user_profile = User.objects.get(pk=user_id).profile
            house_members = house.members
            if (user_profile in house_members.all()):
                house_members.remove(user_profile)
                house.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'User not a member in this house.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({'detail': 'Provided user_id does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
