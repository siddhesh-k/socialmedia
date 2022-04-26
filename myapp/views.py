from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def home(request):
    return render(request,'home.html')

def signIn(request):
    return render(request,'sign_in.html')

def create(request):
    if request.method == "POST":
        username = request.POST['name']
        firstname = request.POST['first_name']
        last_name = request.POST['last_name']
        password= request.POST['password']
        profile_picture = request.POST['profile_picture']
        email= request.POST['email']
        mobile= request.POST['mobile']
        obj = User.objects.create(username=username,first_name= firstname,last_name=last_name,
                                  password=password,profile_picture=profile_picture,
                                  email=email,mobile=mobile)
        obj.save()
        return redirect('/signup')