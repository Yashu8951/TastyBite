from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer

def home(request):
    return render(request,'html/home.html')
# Create your views here.

def open_signin(request):
    return render(request,'html/Login.html')

def open_signup(request):
    return render(request,'html/Register.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        
        Customer.objects.create(username = username,
                                password = password,
                                email=email,
                                mobile =mobile,
                                address = address)
    return render(request,'html/Login.html')