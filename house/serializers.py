from rest_framework import serializers
from . models import House
from users.models import Profile

class HouseSerializer(serializers.ModelSerializer):
    
    members_count = serializers.IntegerField(read_only=True, default=0)
    #HYPERLINK
    manager  = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name = 'profile-detail')
    #HYPERLINK and DROP DOWN
    #manager  = serializers.HyperlinkedRelatedField(queryset=Profile.objects.all(), many=False, view_name = 'profile-detail')
    members = serializers.HyperlinkedRelatedField (read_only=True, many=True, view_name='profile-detail')
    tasklists = serializers.HyperlinkedRelatedField (read_only=True, many=True, view_name='tasklist-detail')
                     
    class Meta:
        model = House        
        fields = ('url', 'id', 'name','image','description', 'created_on', 
          'manager','members_count','points', 'completed_tasks_count' , 'notcompleted_tasks_count','members','tasklists')#'members','tasklists'

        #'members_count' - field not in DB

        read_only_fields = ('points', 'completed_tasks_count' , 'notcompleted_tasks_count')#,'members'



"""
from rest_framework import serializers
from . models import House

class HouseSerializer(serializers.ModelSerializer):

    members_count = serializers.IntegerField(read_only=True) 
    manager = serializers.HyperlinkedRelatedField (read_only=True, many=False, view_name='profile-detail') 
    # ???????????????????????++ so when are you going to add MANAGER if it is READ_ONLY
     

    #see MODELS.PY (TASK APP) Model TaskList
    #house = models.ForeignKey ('house.House', on_delete=models.CASCADE, related_name="tasklists") 
    #RELATED_NAME

          
    class Meta:
        model = House
        fields = ('url', 'id', 'name', 'image', 'created_on', 'description',
         'members', 'manager', 'members_count', 'points', 'completed_tasks_count' , 'notcompleted_tasks_count', 'tasklists')


        read_only_fields = ('points', 'completed_tasks_count' , 'notcompleted_tasks_count','members')
"""




 

  
