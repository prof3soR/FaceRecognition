from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    name = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=10, unique=True)
    dept = models.CharField(max_length=255)
    section = models.CharField(max_length=10)
    face_encoding = models.BinaryField(null=True, blank=True)
    def __str__(self):
        return self.name
    

class working_day(models.Model):
    date=models.DateField()
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    

class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date} {self.student}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
