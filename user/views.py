from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import response
from django.views.decorators.csrf import csrf_exempt  # import the decorator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from  django.contrib.auth.decorators import login_required
from django.db import IntegrityError


# Create your views here.
@login_required
def HomePage(request):
    return render(request, 'user/homepage.html', {})
@csrf_exempt
def Register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')
        if password == cpassword:
            if len(password) > 7:
                try:
                    new_user = User.objects.create_user(uname, email, password)
                    new_user.first_name = fname
                    new_user.last_name = lname
                    new_user.save()
                    return redirect('login')
                except IntegrityError:
                    error_message = "Username already exists. Please choose a different username."
                    return render(request, 'user/register.html', {'error_message': error_message})
        error_message = "Passwords do not match or password length is less than 8 characters."
        return render(request, 'user/register.html', {'error_message': error_message})
    return render(request, 'user/register.html', {})

@csrf_exempt
def Login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=uname,password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        '''return HttpResponse(
            {'Invalid username or password'})'''
        return redirect('login')
    return render(request, 'user/login.html', {})
def Logout(request):
    logout(request)
    return redirect('login')
def About(request):
    return render(request, 'user/about.html', {})