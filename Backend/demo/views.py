from django.shortcuts import render, HttpResponse
from .models import TestData

# Create your views here.

def home(request):
    items = TestData.objects.all()
    return render(request, "home.html", {"data":items})
