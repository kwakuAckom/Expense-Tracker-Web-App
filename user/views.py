from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import response
from django.views.decorators.csrf import csrf_exempt  # import the decorator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from  django.contrib.auth.decorators import login_required
from django.db import IntegrityError


# Home page view, decorator to restrict access to logged in users only
@login_required
def HomePage(request):
    return render(request, 'user/homepage.html', {})

# Register view, csrf_exempt decorator is added to bypass the CSRF token requirement for POST requests
@csrf_exempt
def Register(request):
    if request.method == 'POST':
        # Get the form data
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')
        # Validate the password and create a new user if valid
        if password == cpassword:
            if len(password) > 7:
                try:
                    # Create the new user and save the details
                    new_user = User.objects.create_user(uname, email, password)
                    new_user.first_name = fname
                    new_user.last_name = lname
                    new_user.save()
                    # Redirect the user to the login page after successful registration
                    return redirect('login')
                except IntegrityError:
                    # If the username already exists, show an error message
                    error_message = "Username already exists. Please choose a different username."
                    return render(request, 'user/register.html', {'error_message': error_message})
        # If the password is invalid or the passwords don't match, show an error message
        error_message = "Passwords do not match or password length is less than 8 characters."
        return render(request, 'user/register.html', {'error_message': error_message})
    # If the request is not a POST request, show the registration form
    return render(request, 'user/register.html', {})

# Login view, csrf_exempt decorator is added to bypass the CSRF token requirement for POST requests
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        # Get the username and password from the form data
        uname = request.POST.get('uname')
        password = request.POST.get('pass')
        # Authenticate the user
        user = authenticate(request, username=uname,password=password)
        if user is not None:
            # If the user is authenticated, log them in and redirect them to the home page
            login(request, user)
            return redirect('homepage')
        # If the authentication fails, redirect the user to the login page
        return redirect('login')
    # If the request is not a POST request, show the login form
    return render(request, 'user/login.html', {})

# Logout view
def Logout(request):
    # Log the user out and redirect them to the login page
    logout(request)
    return redirect('login')

# About view
def About(request):
    return render(request, 'user/about.html', {})
