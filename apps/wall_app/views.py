"""import"""
from django.shortcuts import render, redirect
from apps.login_app.models import User
from .models import Message, Comment


def wall(request):
    """Wall Page"""
    if "logged_user" in request.session:
        context = {
            "user_name": User.objects.get_user_name(request.session['logged_user']),
            "messages": Message.objects.all(),
            "message_check": Message.objects.check_time(),
            "comment_check": Comment.objects.check_time()
        }
        return render(request, "wall_app/wall.html", context)
    return redirect("/")


def create_message(request):
    """Create Message Method"""
    if request.method == "POST":
        Message.objects.create_message(
            request.POST, request.session['logged_user'])
    return redirect("/wall")


def remove_message(request, number):
    """Remove Message Method"""
    Message.objects.remove_message(number)
    return redirect("/wall")


def create_comment(request):
    """Create Comment Method"""
    if request.method == "POST":
        Comment.objects.create_comment(
            request.POST, request.session['logged_user'])
    return redirect("/wall")


def remove_comment(request, number):
    """Remove Comment Method"""
    Comment.objects.remove_comment(number)
    return redirect("/wall")
