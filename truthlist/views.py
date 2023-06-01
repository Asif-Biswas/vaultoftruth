from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from .models import *



# Create your views here.

def home(request):
    
    return render(request,'truthlist/home.html')

def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # read the excel file
        df = pd.read_excel(file)
        # check the second column name is question
        if df.columns[1].lower() != 'question':
            messages.error(request, "The second column name should be Question")
            return redirect('upload')
        # check the third column name is category
        if df.columns[2].lower() != 'category':
            messages.error(request, "The third column name should be Category")
            return redirect('upload')
        # check the fourth column name is fundamentals
        if df.columns[3].lower() != 'fundamentals':
            messages.error(request, "The fourth column name should be Fundamentals")
            return redirect('upload')
        # convert the dataframe into list
        df = df.values.tolist()
        for row in df:
            q = Question.objects.get_or_create(question=row[1])[0]
            q.category = Category.objects.get_or_create(name=row[2])[0] if row[2] else None
            q.is_fundamental = True if row[3] and row[3].lower() == 'yes' else False
            q.save()

        messages.success(request, "Questions uploaded successfully")

    return render(request, 'truthlist/upload.html')


def profile(request):
    questions = UserAnswer.objects.filter(user=request.user)
    return render(request, 'truthlist/profile.html', {'questions': questions})


def assessment(request):
    questions = Question.objects.filter(active=True)
    if request.method == 'POST':
        for q in questions:
            answer = request.POST.get(str(q.id))
            if answer:
                ua = UserAnswer.objects.get_or_create(user=request.user, question=q)[0]
                ua.answer = answer
                ua.save()
        
        return redirect('profile')
    return render(request, 'truthlist/assessment.html', {'questions': questions})


def add_to_certificate(request, id, value):
    ua = UserAnswer.objects.get(id=id)
    if value == 'true':
        ua.add_to_certificate = True
    else:
        ua.add_to_certificate = False
    ua.save()
    return redirect('profile')


def add_new_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        category = request.POST.get('category')
        is_fundamental = True if request.POST.get('is_fundamental') == 'on' else False
        if question:
            q = Question.objects.get_or_create(question=question)[0]
            q.category = Category.objects.get(id=category) if category else None
            q.is_fundamental = is_fundamental
            q.save()
            messages.success(request, "Question added successfully")
            return redirect('add_new_question')
        else:
            messages.error(request, "Question is required")
            return redirect('add_new_question')
    
    categories = Category.objects.all()
    return render(request, 'truthlist/add_new_question.html', {'categories': categories})


def pending_questions(request):
    questions = Question.objects.filter(active=False)
    return render(request, 'truthlist/pending_questions.html', {'questions': questions})


def approve_question(request, id):
    q = Question.objects.get(id=id)
    q.active = True
    q.save()
    return redirect('pending_questions')


def reject_question(request, id):
    q = Question.objects.get(id=id)
    q.delete()
    return redirect('pending_questions')


def public_believes(request):
    ua = UserAnswer.objects.all()
    return render(request, 'truthlist/public_believes.html', {'user_answer': ua})


def reasons(request, id):
    return render(request, 'truthlist/reasons.html', {'id': id})







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