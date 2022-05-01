from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import User,Posts,Tag,UserDetails
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
def home(request):
    return render(request,'home.html')

def signIn(request):
    return render(request,'sign_up.html')


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
        username = request.session['username']
        title = request.POST['title']
        poster = request.FILES['poster']
        description = request.POST['description']
        try:
            user= User.objects.get(username=username)
            obj = Posts.objects.create(title=title, description=description,poster=poster,created_by=user)
            # obj.tags.set([tags])
            obj.save()
        except Exception as e:
            print(e)
            return redirect('/')
        def extract_hashtags(text):

            # initializing hashtag_list variable
            hashtag_list = []

            # splitting the text into words
            for word in text.split():

                # checking the first character of every word
                if word[0] == '#':
                    # adding the word to the hashtag_list
                    hashtag_list.append(word[1:])

            # printing the hashtag_list
            print("The hashtags in \"" + text + "\" are :")
            for hashtag in hashtag_list:
                print(hashtag)

        return redirect('/')
    return render(request,'add_post.html')

@login_required(login_url="sign_up")
def show_posts(request):
    posts = Posts.objects.all().order_by('-created_at')

    context ={"posts":posts}
    return  render(request,'show_posts.html', context)

def log_in(request):
    if request.method == "POST":
        username= request.POST["username"]
        password = request.POST["password"]
        user = User.objects.all().filter(username=username)

        if user:
            if user[0].password == password:
                request.session["username"]=username
                request.session['isLoggedIn']=True
                return HttpResponseRedirect('/show_posts')
            else:
                return render(request,'log_in.html', {"error":"Invalid password"})
        else:
            return render(request, 'log_in.html', {"error": "Username Invalid"})
    else:
        return render(request,"log_in.html")

def log_out(request):
    request.session["isLoggedIn"] = False
    request.session['username']=""
    return HttpResponseRedirect('/show_posts')

def account(request):
    try:
        username= request.session["username"]
        user = User.objects.get(username=username)
        userdetails = UserDetails.objects.get(user=user)
        print(userdetails.profile_picture)
        posts = Posts.objects.all().filter(created_by=user.id).order_by('-created_at')

        context = {"posts": posts,
                   "userinfo":user,
                   "userdetail":userdetails
                   }
        return render(request,"account.html",context)
    except Exception as e:
        print(e)
        return redirect("/show_posts")

