from django.db import models
from django.contrib.auth.models import User


import os 
from django.utils.deconstruct import deconstructible
@deconstructible
class GenerateProfileImagePath(object):

	def __init__(self):
		pass

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		path = f'accounts/{instance.user.id}/images/'
		name = f'profile_image.{ext}'
		return os.path.join(path, name)

user_profile_image_path = GenerateProfileImagePath()


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
	house = models.ForeignKey('house.House',on_delete=models.SET_NULL, blank=True, null=True,related_name='members')#related_name='members'
	#house.House - APP.MODEL
	#IF house deleted, do not delete profile, set his house NULL
	#MEMBERS will be used in HOUSE APP serializers.py

	""""
	WAY 2
	from house.models import House
	house = models.ForeignKey(House,on_delete=models.SET_NULL, blank=True, null=True, related_name='members')
	"""

	def __str__(self):
		return f'{self.user.username}\'s Profile'




