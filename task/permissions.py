#SECTION 5, TUTORIAL 45

from rest_framework import permissions

#######################################  TASK LIST ##############################################
# LIST (EVERYONE can GET (hidden with MIXINS), only AUTH (logged on) can POST), INSTANCE (only who created can edit Task List)

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):

    #GET, POST (see LIST)
    def has_permission(self, request, view):
        
        #GET - everyone can see list (regardless if user aAUTh or not)
        if request.method in permissions.SAFE_METHODS:
            return True

        #POST - only if AUTH
        if not request.user.is_anonymous:
            return True

        return False #if returned false has_object_permission() will never be called

    def has_object_permission(self, request, view, obj):

        #WHAT ABOUT GET ???? At the moment,  "detail": "You do not have permission to perform this action."
        """YOU HAVE TO ADD THIS
        if request.method in permissions.SAFE_METHODS:
            return True
        """
        
        #PUT and PATCH  and  DELETE 
        #AUTH checed ABOVE in has_permission()
        return request.user.profile == obj.created_by #only who created can edit 
        #AUTH done in has_permission() ABOVE

#####################################     TASK  SECTION 5, TUTORIAL 48   ##############################################
#you can GET and POST as far as you ate AUTH (logged on) 
#you can edit tasks which belog to same house (via task list) as you. You MUST NOT created the task (only be in same house)
# you can EDIT (as well GET)  only TASK which belongs to same HOUSE (via TASKLIST) as you (PROFILE)   

class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    
    #Custom permissions for TaskViewSet to only allow members of a house access to its tasks.   

    def has_permission(self, request, view):

        if not request.user.is_anonymous: #not done SAFE_MODE, does this apply both GET and POST??????????
            return request.user.profile.house != None   #USER must be part of any house

        return False
        #*********************************************************
        #SHOULD SEE (GET) ONLY TASKS CREATED BY YOU 
        #see SERIALIZERS.PY, Custom tailored queryset
        #********************************************************
        
    def has_object_permission(self, request, view, obj):
        
        return request.user.profile.house == obj.task_list.house


#####################################     ATTACHMENT  SECTION 5, TUTORIAL 48  ##############################################
#can GET and POST if AUTH
class IsAllowedToEditAttachmentElseNone(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_anonymous: #not done SAFE_MODE
            return request.user.profile.house != None # User must be part of a house

        return False

   #can EDIT only ATTACHMENT from same HOUSE as USER
    def has_object_permission(self, request, view, obj):
        
        return request.user.profile.house == obj.task.task_list.house
