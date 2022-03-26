from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from . serializers import UserSerializer, ProfileSerializer
from . permissions import IsUserOwnerOrGetAndPostOnly , IsProfileOwnerOrGetAndPostOnly
from . models import Profile
#from users import permissions

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserOwnerOrGetAndPostOnly ,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    #We want only to RETRIEVE and UPDATE profile 
    #class ProfileViewSet(viewsets.ModelViewSet):    
    permission_classes = (IsProfileOwnerOrGetAndPostOnly ,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
