from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver #DECORATOR to help us to convert normal function into signal
from .models import Task, COMPLETE, NOT_COMPLETE #variables

#EVERYTHING IS GOING VIA TASK model

#add 10 POINTS to house when Task completed 
@receiver(post_save, sender=Task) 
def create_house_points(sender, instance, created, **kwargs):
    #will run every time something happen to an instance of Task obj inside our DB after it has been saved

    #get House that Task coresponses to
    house = instance.task_list.house
    if instance.status == COMPLETE:
        house.points += 10
    elif instance.status == NOT_COMPLETE:
        if house.points>10:
            house.points -= 10
    house.save()

##################################  TESKO MALO  #############################################################
#status 
#completed_on ?


#change TaskList status to COMPLETE once ALL Tasks (in TaskList) have been completed (LOOP)
@receiver(post_save, sender=Task) 
def update_tasklist_status(sender, instance, created, **kwargs):
    #will run every time something happen to an instance of TaskList obj inside our DB after it has been saved

    task_list = instance.task_list
    is_complete = True
    for task in task_list.tasks.all():
        if task.status != COMPLETE: #enough that 1 is not completed, come out of LOOP
            is_complete = False
            break
    
    #HIS WAY
    #task_list.status = COMPLETE if is_complete else NOT_COMPLETE
    
    if is_complete:
        task_list.status = COMPLETE
    else:
        task_list.status = NOT_COMPLETE
    
    task_list.save()

