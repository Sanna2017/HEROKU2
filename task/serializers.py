from rest_framework import serializers
from . models import TaskList, Task, Attachment
from house.models import House

class TaskListSerializer(serializers.ModelSerializer):

    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')    
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), many=False, view_name='house-detail')
    tasks = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='task-detail')

    class Meta:
        model = TaskList
        fields = ('url', 'id', 'name', 'description', 'status', 'created_on',
        'created_by', 'completed_on', 'house','tasks') #'tasks' 
        # 'completed_on'  - did no use, but in model did

        #Whoever sent POST (create TAskList) that user (taken out from request) is going to be created_by

        read_only_fields = ('completed_on','status' )  #see above CREATED_BY read_only

####################################################################################

class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name = 'profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name = 'profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name = 'tasklist-detail')
    attachments = serializers.HyperlinkedRelatedField (read_only=True, many=True, view_name='attachment-detail') 
    # ATTACHMENTS see RELATED_NAME model Attachment, LINK TO IMAGE

    class Meta:
        model = Task
        fields = ('url', 'id', 'name', 'description', 'status', 'created_on',
        'created_by', 'completed_on', 'completed_by', 'task_list','attachments')   #'attachments' see models related_name

        read_only_fields = ('completed_on', ) # SEE ABOVE META - 'created_by' , 'completed_by'
    
    
    #same function applied to all 3x methods – POST, PUT; PATCH 
    #compare to password (POST needs password)(PUT and PATCH need old_password as well)
    def validate_task_list(self, value):
        user_house = self.context['request'].user.profile.house
        #HIS WAY
        #if value not in user_profile.house.lists.all(): #all TaskList for a specific House
        if value.house != user_house: #MY WAY
            raise serializers.ValidationError(
                "Tasklist provided does not belong to house for which user is member.")
        return value

   
    def create(self, validated_data): #name, description, task_list
        user_profile = self.context['request'].user.profile
        task = Task.objects.create(**validated_data)
        task.created_by = user_profile
        task.save()
        return task

#####################################################################################

class AttachmentSerializer(serializers.ModelSerializer):

    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name='task-detail')
    
    def validate_task (self, value): 
        user_house = self.context['request'].user.profile.house
        if value.task_list.house != user_house: 
            raise serializers.ValidationError(
                "Task selected does not belong to house for which user is member.")
        return value

    class Meta:
        model = Attachment
        fields = ('url', 'id', 'created_on', 'data', 'task')

        #read_only_fields = ('created_on', ) auto read only


    """ #MUST GO ABOVE META #
    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs['task']
        task_list = TaskList.objects.get(tasks__id__exact=task.id)
        if task_list not in user_profile.house.lists.all():
            raise serializers.ValidationError(
                {"task": "Task provided does not belong to house for which user is member."})
        return attrs
    """

      
