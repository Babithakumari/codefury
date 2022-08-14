from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Startup,Order
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import razorpay
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
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
def investments(request):
    

    user = User.objects.get(username=request.user.username)
    investments = user.investments.all()
    print(investments)

    return render(request, "innovate/investments.html",{
        "startups":investments

    })
def invest(request):
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'innovate/index.html', context=context)


@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()



def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "innovate/order.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    return render(request, "innovate/order.html")



@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "innovate/callback.html", context={"status": order.status})




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
