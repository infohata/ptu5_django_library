from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# funckiniai viewsai visalaik reikalauja requesto (funkcijoj)

def index(request):
    return HttpResponse("Sveiki atvyke!")



