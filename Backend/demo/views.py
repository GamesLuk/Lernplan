from django.shortcuts import render, HttpResponse
from .models import TestData
from django.views.decorators.cache import cache_page

# Create your views here.

@cache_page(60 * 10)
def home(request):
    items = TestData.objects.all()
    return render(request, "home.html", {"data":items})
