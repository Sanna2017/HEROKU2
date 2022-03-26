from rest_framework import permissions

#SECTION 4, TUTORIAL 31
class IsHouseManagerOrNone(permissions.BasePermission):
    #  only allow specific privileges for editing specific house attributes 

    #GET, POST (see LIST)
    def has_permission(self, request, view):
        
        #GET - everyone can see list
        if request.method in permissions.SAFE_METHODS:
            return True

        #POST - only if AUTH (logged on). User we allowed because as new user you are none AUTH 1st time.
        if not request.user.is_anonymous:
            return True

        #return False #if returned false has_object_permission() will never be called



    def has_object_permission(self, request, view, obj):

        #GET instance, ANYONE
        if request.method in permissions.SAFE_METHODS:
            return True

        #PUT, PATCH, DELETE, only MANAGER
        return request.user.profile == obj.manager

         #if not request.user.is_anonymous:
        #THIS PART IS NOT DONE AS IT IS DONE IN has_permission() ABOVE
