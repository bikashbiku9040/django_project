"""import"""
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def index(request):
    """Home Page"""
    return render(request, "login_app/index.html")


def success(request):
    """Success Page"""
    if "logged_user" in request.session:
        context = {
            "user_name": User.objects.get_user_name(request.session['logged_user'])
        }
        return render(request, "login_app/success.html", context)
    return redirect("/")


def register(request):
    """Register Method"""
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            # display errors
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/")
        request.session['logged_user'] = User.objects.create_user(request.POST)
        return redirect("/success")
    return redirect("/")


def login(request):
    """Login Method"""
    if request.method == "POST":
        user_id = User.objects.get_user_id(request.POST)
        if user_id:
            request.session['logged_user'] = user_id
            return redirect('/success')
        # display login error
        messages.error(request, "This user does not exist!", extra_tags="login_error")
    return redirect("/")


def logout(request):
    """Logout Method"""
    if "logged_user" in request.session:
        del request.session["logged_user"]
    return redirect("/")
