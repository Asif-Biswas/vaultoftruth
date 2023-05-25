from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
from .models import UserData
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import os
from django.core.files.storage import default_storage
from django.conf import settings
import json



# Create your views here.

def home(request):
    # Get the path to the Excel file in the same folder as manage.py
    file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Questions.xlsx'))

    # Read the Excel file and convert it to a list
    data = pd.read_excel(file_path)
    data_list = data.values.tolist()

    if request.method == 'POST':
        result = []
        for d in data_list:
            result.append([
                d[1],
                request.POST.get(str(d[0]))
            ])
        
        # Save the result to the database
        user_data = UserData.objects.get_or_create(user=request.user)[0]
        user_data.data = json.dumps(result)
        user_data.save()
        return redirect('profile')
    
    return render(request,'truthlist/home.html', {'data_list': data_list})

def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = 'Questions.xlsx'  # Name of the file to be saved

        # Define the path to the existing file
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Save the uploaded file, overwriting the existing file if it exists
        with open(file_path, 'wb') as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)

            messages.success(request, "File uploaded successfully")

    return render(request, 'truthlist/upload.html')


def profile(request):
    user_data = UserData.objects.filter(user=request.user).last()
    return render(request, 'truthlist/profile.html', {'user_data': user_data})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("home")
        else:
            # No backend authenticated the credentials
            messages.error(request, "Invalid Credentials")
            return render(request, "truthlist/login.html")
    return render(request, "truthlist/login.html")

def logout_view(request):
    logout(request)
    return render(request, "truthlist/login.html")

def register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "truthlist/register.html")
        if len(password) < 8:
            messages.error(request, "Password must be atleast 8 characters long")
            return render(request, "truthlist/register.html")
        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return render(request, "truthlist/register.html")
        
        user = User.objects.create_user(email, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        messages.success(request, "Account created successfully")
        return render(request, "truthlist/login.html")
        
    return render(request, "truthlist/register.html")