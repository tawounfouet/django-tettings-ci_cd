from django.shortcuts import render, get_object_or_404
from .models import Letting


def index(request):
    """Display all lettings."""
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


def detail(request, letting_id):
    """Display details of a specific letting."""
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/detail.html", context)
