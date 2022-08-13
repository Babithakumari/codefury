from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Startup
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.db.models import Q

# Create your views here.
def index(request):
    # get all startup ideas
    all_startups = Startup.objects.order_by("-timestamp").all()
    return render(request, "innovate/index.html",{
        "startups":all_startups
        
    })

def create(request):
    if request.method == "POST":
        # validate new startup
        n = request.POST["title"]
        d = request.POST["description"]
        s = request.POST["subject"]
        new_startup = Startup(name=n, description=d, subject=s, founder=request.user)
        new_startup.save()
        return HttpResponseRedirect(reverse("index"))


    return render(request, "innovate/create.html")


def edit(request,s_id):

    if request.method=="POST":
        n = request.POST["title"]
        d = request.POST["description"]
        s = request.POST["subject"]
        new_startup = Startup.objects.filter(pk=s_id).update(name=n, description=d, subject=s, founder=request.user)
        return HttpResponseRedirect(reverse("index"))

        

    startup=Startup.objects.get(pk=s_id)
    return render(request,"innovate/edit.html",{
        "startup":startup
    })

def delete(request,s_id):
    startup = Startup.objects.get(pk=s_id)
    startup.delete()
    return HttpResponseRedirect(reverse("index"))

def search(request):
    if request.method=="POST":
        s_word = request.POST["s_word"]
        matching_startups = Startup.objects.filter(name__icontains=s_word) | Startup.objects.filter(subject__icontains=s_word)
        return render(request,"innovate/search.html",{
            "startups":matching_startups
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "innovate/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "innovate/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "innovate/register.html")
