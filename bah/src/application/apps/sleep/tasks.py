from time import sleep
from application.celery import app
from celery import shared_task

from .models import Sleeper


@shared_task
def sleeping_task(sleeper_id):
    sleeper = Sleeper.objects.get(id=sleeper_id)
    print(sleeper)

    try:
        for i in range(sleeper.input):
            sleep(1)
            sleeper.time_asleep = i+1
            sleeper.save()
            print("Asleep for",sleeper.time_asleep)
        sleeper.status = Sleeper.STATUS_SUCCESS
    except Exception as e:
        sleeper.status = Sleeper.STATUS_ERROR
        sleeper.message = str(e)[:110]
    
    sleeper.save()
