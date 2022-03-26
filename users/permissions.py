#Section 3, TUTORIAL 19
from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    #LIST - anyone (even not AUTH) can GEt and POST (create new user)
    #INSTANCE - anyone (even not AUTH) can GET instance, but only AUTH OWNER can Put,PATCH,DELETE


    #POST,GET (so new user can be added with POST) 
    #anyone (even not AUTH) can GET and POST list (create a new user)
    def has_permission(self, request, view): #this function() is called for API methods - GET and POST 
        return True #if FALSE, has_object_permission() cannot run
     #IF has_permission() returns FALSE, has_object_permission() will never be called


    #access to INSTANCE 
    def has_object_permission(self, request, view, obj): #when you go to INSTANCE

        #GET - will give access to GET, see INSTANCE even in not AUTH
        if request.method in permissions.SAFE_METHODS: #SAFE_METHODS: GET, HEAD, OPTIONS
            return True

        if not request.user.is_anonymous: #if AUTH
            return request.user == obj  #OWNER have full access  (DELETE,PATCH,PUT) to OBJ

        # compare to the actual object. Object of VIEWSET we placed this permission on, 
        # since we are going to be placing this permission on  UserViewSet            permission_classes = (IsUserOwnerOrGetAndPostOnly ,)
        # object in this case is going to be the user model object

        return False




#section 3, TUTORIAL 26
class IsProfileOwnerOrGetAndPostOnly(permissions.BasePermission):

    def has_permission(self, request, view): 
        return True 

    def has_object_permission(self, request, view, obj): 
        #GET - anyone can GET instance
        if request.method in permissions.SAFE_METHODS: 
            return True

        # only AUTH owner can PUT,PATCH
        if not request.user.is_anonymous:
            return request.user.profile == obj

        return False
