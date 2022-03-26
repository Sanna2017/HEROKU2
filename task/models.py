from django.db import models

NOT_COMPLETE = 'NC'
COMPLETE = 'C'
TASK_STATUS_CHOICES = [
    (NOT_COMPLETE, 'Not Completed'),
    (COMPLETE, 'Complete')
]

class TaskList (models.Model):

    name = models.CharField(max_length = 120)
    description = models.TextField(null=True, blank = True) #optional
    status = models.CharField(
        max_length=2,
        choices=TASK_STATUS_CHOICES,
        default=NOT_COMPLETE,
    )
    created_on = models.DateTimeField(auto_now_add=True)  
    created_by = models.ForeignKey ('users.Profile', on_delete=models.SET_NULL, null=True, blank = True) #related_name='lists'
    completed_on = models.DateTimeField(null=True, blank = True) 
    house = models.ForeignKey('house.House', on_delete=models.CASCADE, related_name='tasklists') #related_name='tasklists'

    def __str__(self):
        return f'{self.id} | {self.name}'

#########################################################

class Task (models.Model):
        
    name = models.CharField(max_length = 120)
    description = models.TextField(null=True, blank = True) #optional
    status = models.CharField(
        max_length=2,
        choices=TASK_STATUS_CHOICES,
        default=NOT_COMPLETE,
    )
    
    created_on = models.DateTimeField(auto_now_add=True)  
    created_by = models.ForeignKey ('users.Profile', on_delete=models.SET_NULL, null=True, blank = True) #related_name="created_tasks"
    #if profile deleted, task should not be deleted
    completed_on = models.DateTimeField(null=True, blank = True) # OK to be empty 
    completed_by = models.ForeignKey ('users.Profile', on_delete=models.SET_NULL, null=True, blank = True, related_name='completed_task') #related_name='completed_task'
    #RELATION CHASHHHHHHHHHHHHHHHHHHHHHH
    task_list = models.ForeignKey('task.TaskList', on_delete=models.CASCADE, related_name='tasks') #related_name='tasks'
    #if TASKLIST deleted, TASK deleted as well
 
    def __str__(self):
        return f'{self.id} | {self.name}'


#############################################################################

from django.utils.deconstruct import deconstructible
import os
import uuid
@deconstructible
class GenerateAttachmentFilePath(object):

    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'tasks/{instance.task.id}/attachments'
        #path = f'media/tasks/{instance.task.id}/attachments'
        name = f'{instance.id}.{ext}'
        return os.path.join(path, name)

attachment_file_path = GenerateAttachmentFilePath()

#######################  MODEL ATTACHMENT ########################################
class Attachment (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # we do not want to edit ID
    created_on = models.DateTimeField(auto_now_add=True) 
    data = models.FileField(upload_to=attachment_file_path) 
    task = models.ForeignKey ('task.Task', on_delete=models.CASCADE,related_name="attachments") #related_name="attachments"

    def __str__(self):
        return f'{self.id} | {self.task}'

