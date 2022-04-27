from django.shortcuts import render, redirect
from .models import User,Posts,Tag

# Create your views here.
def home(request):
    return render(request,'home.html')

def signIn(request):
    return render(request,'sign_in.html')


def create_user(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['first_name']
        last_name = request.POST['last_name']
        password= request.POST['password']
        email= request.POST['email']
        obj = User.objects.create(username=username,first_name= firstname,last_name=last_name,password=password,email=email)
        obj.save()
        return redirect('/')

def add_post(request):

    if request.method == "POST":
        print(request.FILES)
        title = request.POST['title']
        poster = request.FILES['poster']
        description = request.POST['description']
        try:
            user= User.objects.get(pk=1)
            obj = Posts.objects.create(title=title, description=description,poster=poster,created_by=user)
            # obj.tags.set([tags])
            obj.save()
        except Exception as e:
            print(e)
            return redirect('/')

        return redirect('/')
    return render(request,'add_post.html')
