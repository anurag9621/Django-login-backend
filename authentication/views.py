from email import message
from login import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if User.objects.filter(username=username):
            messages.error(request, "Username is already exist ")
        if User.objects.filter(email=email):
            messages.error(request, "Email already exist")
            return redirect('home')
        if len(username) > 10:
            messages.error(request, "Username is too long")
        if(cpassword != password):
            messages.error(request, "Passwords diden't match")
        if not username.isalnum():
            messages.error(request, " Username must be Alpha-Numeric")
            return redirect("home")

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(
            request, "Your are Registered Please Conform Your Email ")

        subject = "Welcome to are website "
        message = "Hello " + myuser.first_name + " !!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credentials !")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "logout")
    return redirect('home')
