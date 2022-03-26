from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver #DECORATOR to help us to convert normal function into signal

from .models import Profile

#AUTOMATING USER PROFILE CREATION # Section 3,12 
@receiver(post_save, sender=User) #every time someting happen to User model....
def create_user_profile(sender, instance, created, **kwargs):
    if created: #TRUE when User obj created 1st time in DB
        Profile.objects.create(user=instance) #instance passed in function()


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    #SENDER is USER MODEL
    if not instance.username: #If username does not exist, OF COURSE THAT IT DOES NOT EXIST AS THEY DID NOT HAVE POSSIBILITY TO ENTER IT
        username = f'{instance.first_name}_{instance.last_name}'.lower()
        #instance.username = username  #WILL NOT WORK IF USERNAME ALREADY EXISTS, DONE BELOW
        counter = 1
        while User.objects.filter(username=username): #FILTER username same as this one (can be only 1 match)
            username = f'{instance.first_name}_{instance.last_name}_{counter}'.lower()
            counter += 1 #increment after so 1st starts with 1, for next time
        instance.username = username
        #instance.save() NOOOOOOOOOOOOOOOOO as this is PRE_SAVE SIGNAL
        #DJANGO will call SAVE later on in life cycle of model instance

        #INSTANCE is our USER MODEL 
