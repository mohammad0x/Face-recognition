from .models import *
from .views import *
from celery import shared_task
import os
import shutil
import threading

folder_path = './media/unknow/'
folder_path1 = './media/old/'
try:
    Getdate.objects.create(text='remove')
except:
    pass


@shared_task
def attendance():
    res = Result.objects.filter(noise=False)
    for result in res:
        try:
            Attendance.objects.create(user_id=result.id, check_in_date=jdatetime_datetime.now().strftime('%d %B %Y'))
        except:
            pass
        delete_folder_contents(folder_path)
        break


def delete_folder_contents(folder_path):
    date = Getdate.objects.all()
    for date in date:
        res = date.date_time
        result = res.split(" ")
        if int(result[0]) == int(result[0]) + 2:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            for filename in os.listdir(folder_path1):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

# 00000000000000000000000000000000000000000000000000000000000000000000000000
