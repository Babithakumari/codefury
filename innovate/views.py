from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Startup
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    # get all startup ideas
    all_startups = Startup.objects.order_by("-timestamp").all()
    user = User.objects.get(username=request.user.username)
    favourites = user.favourites.all()
    return render(request, "innovate/index.html",{
        "startups":all_startups,
        "favourites":favourites
        
    })

def create(request):
    if request.method == "POST" and request.FILES['image'] and request.FILES['plan']:
        # validate new startup
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        image_url = fss.url(file)

        plan = request.FILES['plan']
        fss = FileSystemStorage()
        file = fss.save(plan.name, plan)
        plan_url = fss.url(file)

        n = request.POST["title"]
        d = request.POST["description"] 
        
        new_startup = Startup(name=n, description=d, image=image_url, business_plan=plan_url, founder=request.user)
        new_startup.save()
        return HttpResponseRedirect(reverse("index"))


    return render(request, "innovate/create.html")


def edit(request,s_id):

    if request.method == "POST":
        s_obj= Startup.objects.get(pk=s_id)
        if request.FILES['image']!='':
            # validate new startup
            image = request.FILES['image']
            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            image_url = fss.url(file)
        else:
            image_url = s_obj.image
        if request.FILES['plan']:
            plan = request.FILES['plan']
            fss = FileSystemStorage()
            file = fss.save(plan.name, plan)
            plan_url = fss.url(file)
        else:
            plan_url=s_obj.business_plan

        n = request.POST["title"]
        d = request.POST["description"] 
        new_startup = Startup.objects.filter(pk=s_id).update(name=n, description=d,image=image_url, business_plan=plan_url)

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
        matching_startups = Startup.objects.filter(name__icontains=s_word) 
        return render(request,"innovate/search.html",{
            "startups":matching_startups
        })
def favourites(request):
    if request.method=="POST":
        s_id = request.POST["s_id"]
        s_obj = Startup.objects.get(pk=s_id)
        user =  User.objects.get(username=request.user.username)
        user.favourites.add(s_obj)
        return HttpResponseRedirect(reverse("index"))





    user = User.objects.get(username=request.user.username)
    all_favourites = user.favourites.order_by("-timestamp").all()
    return render(request,"innovate/favourites.html",{
            "startups":all_favourites
        })

    
def startup(request,s_id):
    startup = Startup.objects.get(pk=s_id)
    members = startup.members.all(),
    
    investors = startup.investors.all()
    return render(request, "innovate/startup.html",{
        "startup":startup,
        "members":members,
        "investors":investors
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
