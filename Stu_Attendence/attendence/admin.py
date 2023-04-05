from django.contrib import admin

# Register your models here.
from .views import *

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(working_day)