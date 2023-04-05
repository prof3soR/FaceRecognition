"""Stu_Attendence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from attendence import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("index",views.index,name="index"),
    path("",views.login_view,name="login"),
    path("add_student",views.add_student,name="add_student"),
    path("add_attendance",views.add_attendance,name="add_attendence"),
    path("add_working_day",views.add_working_day,name="add_working_day"),
    path("logout",views.logout_view,name="logout"),
    path("show_attendence",views.show_attendence,name="show_attendence")
]
