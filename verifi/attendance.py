from .models import *
from .views import *
from celery import shared_task

@shared_task
def attendance():
    res = Result.objects.filter(noise=False)
    for result in res:
        Attendance.objects.create(user_id = result.id,check_in_date=jdatetime_datetime.now().strftime('%d %B %Y') )
        print("aaa")
        break

# celery -A FaceGuard worker -l info