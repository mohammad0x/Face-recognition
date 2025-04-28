from django.contrib import admin
from .models import *


# Register your models here.

class adminAttendance(admin.ModelAdmin):
    list_display = ('check_in_time', 'check_in_date', 'user')
    list_filter = ('check_in_time', 'check_in_date', 'user')


admin.site.register(Attendance, adminAttendance)


class adminResult(admin.ModelAdmin):
    list_display = ('name' , 'recognition' , 'date' , 'time')
    list_filter = ('date' , 'time' , 'noise')
    search_fields = ['name']


admin.site.register(Result, adminResult)


class adminlog(admin.ModelAdmin):
    list_display = ('name' , 'status' , 'time')
    list_filter = ['time']
    search_fields = ['name']


admin.site.register(log, adminlog)

admin.site.register(Dbmodel)
