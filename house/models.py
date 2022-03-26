from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
import os 
import uuid

from django.utils.deconstruct import deconstructible
@deconstructible
class GenerateHouseImagePath(object):

	def __init__(self):
		pass

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		path = f'houses/{instance.id}/images/' #delet MEDIA so it does not appear 2x
		name = f'main.{ext}'
		return os.path.join(path, name)

house_image_path = GenerateHouseImagePath()

class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 150)
    image = models.FileField(upload_to=house_image_path, blank=True, null=True)	
    created_on = models.DateTimeField(auto_now_add=True) 
    description = models.TextField()
    manager = models.OneToOneField('users.Profile', on_delete=models.SET_NULL, blank=True, null=True,related_name='managed_house')#related_name='managed_house'
    #REALTIONS CLASHHHHHHHHHHHHHHHHHHHHHH
    # #1:1 a house has 1 manager, user/profile can be manager of only 1 house
    # blank=True, null=True - a house can have no manager

    points = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    notcompleted_tasks_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} | {self.name}'

	#members =  LINK TO PROFILE   --------- SERIALISER READ_ONLY
	#members_count (new field not existing in DB) =  COUNT MEMBERS in VIEW  --------- SERIALISER READ_ONLY
	#task_lists = LINK TO TASK LIST --------- SERIALISER READ_ONLY
	

