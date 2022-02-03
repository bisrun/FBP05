from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def insert(request):
    try:
        clear();
    return render(request, 'redis_geo/index.html')