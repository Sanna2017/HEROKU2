from background_task import background #DECORATOR
from background_task.tasks import Task as BT #AS, we have model name Task so we have to differentiate

from house.models import House #model
from task.models import COMPLETE #variable

@background(schedule=10) #10 minutes
def calculate_house_stats(): #function will run periodically
    #calculate how many completed and not_competed tasks are in a house
    for house in House.objects.all():
        total_tasks = 0
        completed_tasks_count = 0
        house_task_lists = house.tasklists.all() #TASKLISTS or LISTS ---------see SOURCE slide 228
        for task_list in house_task_lists:
            total_tasks += task_list.tasks.count()
            completed_tasks_count += task_list.tasks.filter(status=COMPLETE).count()
        house.completed_tasks_count = completed_tasks_count
        house.notcompleted_tasks_count = total_tasks - completed_tasks_count
        house.save()


if not BT.objects.filter(verbose_name='calculate_house_stats').exists(): #verbose_name - name to be saved with in DB
    calculate_house_stats(repeat=BT.DAILY, verbose_name='calculate_house_stats', priority=0)


