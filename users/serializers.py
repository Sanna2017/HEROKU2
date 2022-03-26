from django.contrib.auth.models import User
from rest_framework import serializers

from . models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField (read_only=True, many=False, view_name='user-detail')
    house = serializers.HyperlinkedRelatedField (read_only=True, many=False, view_name='house-detail')

    class Meta:
        model = Profile
        fields = ('url', 'id', 'user', 'image', 'house')


class UserSerializer(serializers.ModelSerializer):

    #username = serializers.CharField(read_only=True)  
    #password = serializers.CharField(write_only=True, required=False)#CANNOT BE BOTH, see extra_kwargs
    old_password = serializers.CharField(write_only=True, required=False)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name','username', 'email', 'password', 'old_password', 'profile')#,'profile'
   
        extra_kwargs = {
            'password': {
                'required': False, #because of PATCH in INSTANCE 
                'write_only': True, 
                'style': {'input_type': 'password'}
            }
        }

        read_only_fields = ('username' ,)

    ##########################################################################################################################

    #works for PUT or PATCH
    def update(self, instance, validated_data): #instance = ENTITY saved in db
        try:
            user = instance
            if 'password' in validated_data: 
            # as update() is used both for PUT and PATCH 
            # If we PATCH e.g. only 1 field (email), password field will not be filled in 
            # so we have to check if password filled in, then we know that this is PUT 
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception("Old password is incorrect.")
                user.save()
        except Exception as err:
            raise serializers.ValidationError({"info": err})

        return super(UserSerializer, self).update(instance, validated_data)
        #To update email, fname and lname. Old and new passwords are POPPED so they will not be part of validated_data.

    ##############################################################################################################################
    #POST, PUT, PATCH
    def validate(self, data): # row data submitted in the form , NOT VALIDATED_DATA
        request_method = self.context['request'].method #check req method
        password = data.get('password', None) #get pass if any, if not then it is None
        if request_method == 'POST':
            if password == None:
                raise serializers.ValidationError ({"info":"Please provide a password"})
        elif request_method == 'PUT' or request_method == 'PATCH':
            old_password = data.get('old_password', None) 
            if password != None and old_password == None: #intended to change password (entered new, but not old)
                raise serializers.ValidationError ({"info":"Please provide the old password"})        
        return data 
