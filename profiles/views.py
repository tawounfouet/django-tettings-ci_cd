from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile


def index(request):
    """Display all profiles."""
    profiles_list = Profile.objects.all()
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


def detail(request, username):
    """Display details of a specific profile."""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    context = {"profile": profile}
    return render(request, "profiles/detail.html", context)
