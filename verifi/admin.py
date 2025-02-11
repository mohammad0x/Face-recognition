from django.contrib import admin
from .models import *


# Register your models here.

class adminAttendance(admin.ModelAdmin):
    list_display = ('check_in_time', 'check_in_date', 'user')
    list_filter = ('check_in_time', 'check_in_date', 'user')


admin.site.register(Attendance, adminAttendance)

admin.site.register(Dbmodel)
admin.site.register(Result)
