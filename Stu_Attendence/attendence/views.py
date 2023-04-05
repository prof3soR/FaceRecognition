import face_recognition
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
import io
import base64
import cv2
from datetime import datetime
from django.http import HttpResponse
import numpy as np
from .models import *
import numpy as np
from PIL import Image, ImageDraw
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.db.models import Count
# Create your views here.
def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
        return render(request,"attendence/index.html")
    else:
        return render(request,"attendence/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
def add_student(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            reg_no = request.POST.get('reg_no')
            dept = request.POST.get('dept')
            section = request.POST.get('section')
            image_file = request.POST.get("Image")
            # process uploaded image file
            img = Image.open(io.BytesIO(base64.b64decode(image_file.split(',')[1])))
            img = img.convert('RGB')
            img.save(f'{name}.jpg')
            # encode face and save to database
            image = face_recognition.load_image_file(f"{name}.jpg")
            face_encoding = face_recognition.face_encodings(image)[0]
            # save student data and face encoding to database
            student = Student(name=name, reg_no=reg_no, dept=dept, section=section, face_encoding=face_encoding)
            student.save()
            return render(request, 'attendence/add_student.html')
        except ValidationError as e:
            return HttpResponse(f"Invalid data: {e}")
    else:
        return render(request, 'attendence/add_student.html')


    
def add_attendance(request):
    if request.method=="POST":
        known_face_encodings = np.array([np.frombuffer(i.face_encoding, dtype=np.float64) for i in Student.objects.all()])
        face_names = [i.name for i in Student.objects.all()]
        image=request.POST.get("image-data")
        img = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
        img = img.convert('RGB')
        img.save('unknown.jpg')
        unknown_image = face_recognition.load_image_file('unknown.jpg')
# Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
        # See http://pillow.readthedocs.io/ for more about PIL/Pillow
        pil_image = Image.fromarray(unknown_image)
        # Create a Pillow ImageDraw Draw instance to draw with
        draw = ImageDraw.Draw(pil_image)

        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            face_encoding = np.frombuffer(face_encoding, dtype=np.float64)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)

            name = "Unknown"
            message=""
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = face_names[best_match_index]

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
            del draw
            stu = Student.objects.get(name=name)
            
            today = date.today()
            
            if Attendance.objects.filter(student=stu, date=today).exists():
                message = "Attendance already added for "
            else:
                new_att = Attendance(student=stu, present=True, date=today)
                new_att.save()
                message="Attendance added for "

        return render(request,"attendence/add_attendence.html",{"stu":stu,"message":message})
    return render(request,"attendence/add_attendence.html")


def index(request):
    return render(request,"attendence/index.html")

def add_working_day(request):
    today = date.today()
    if working_day.objects.filter(date=today).exists():
        return redirect("index")
    else:
        day=working_day(date=today)
        day.save()
        return redirect("index")
    
def show_attendence(request):
    if request.method=="POST":
        reg_no=request.POST.get("reg_no")
        student = Student.objects.get(reg_no=reg_no)
        total_working_days = working_day.objects.all().count()
        present_days = Attendance.objects.filter(student=student, present=True).count()
        attendance_percentage = (present_days / total_working_days) * 100
        context = {
        'student': student,
        'attendance_percentage': attendance_percentage,
        }
        return render(request, 'attendence/show_attendence.html', context)
    else:
        return render(request,"attendence/show_attendence.html")