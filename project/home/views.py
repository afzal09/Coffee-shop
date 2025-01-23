import json
from .constants import PaymentStatus
from .models import Coffee, Orders, Payments
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from project.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
import razorpay
import math
# index url /
def index(request):
    context = {'login':'login'}
    if request.user.is_authenticated:
        context['login'] = 'Logout'
    return render(request,'home/home_index.html',context)

# shop url
@login_required(login_url="/accounts/login/")
def shop(request):
        res = Coffee.objects.all()
        context={
            'cofees':res
        }
        return render(request,'shop/shop_index.html',context)
        pass

# order url
@login_required()
def order(request,id):
    res = Coffee.objects.get(pk=id)
    return render(request,'order/order.html',{'coffee':res})
    #return HttpResponse("<h2> Order Endpoint </h2>")
    pass

# checkout url
@login_required(login_url="/accounts/login/")
def checkout(request):
    if request.method == "POST":
        name = str(request.user)
        amount = 0
        cart = request.session.get('cart')
        if len(list(cart)) > 1:
            for values in list(cart):
                amount += math.floor(float(cart.get(values).get('price')))
        else:
            amount += math.floor(float(cart.get(list(cart)[0]).get('price')))
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 8200, "currency": "INR", "payment_capture": "1"}
        )
        order = Payments.objects.create(
            customer=name, amount=(amount * 82) , provider_order_id=razorpay_order["id"]
        )
        order.save()
        print(order.customer,'\t',order.amount)
        return render(
            request,
            'checkout/payment.html',
            {
                "callback_url": "http://127.0.0.1:8000/checkout/callback/",
                "razorpay_key": RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    return render(request, 'checkout/checkout.html', {})
@csrf_exempt
def checkout_callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Payments.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "checkout/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "checkout/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Payments.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "chcekout/callback.html", context={"status": order.status})
# signup url
def signup(request):
    return render(request,'registration/register.html',{})
    pass


# Auth Endpoint
def auth(request):
    if request.method == 'POST':
        if request.POST.get('email') is not None:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "This username is already taken. Please choose another.")
                return redirect('/accounts/signup')
            user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
            user.save()
            return redirect('/shop')
        else:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is not None:
                login(request,user)
                messages.success(request, "You have successfully logged in!")
                return redirect('/shop')
            else:
                return render(request,'404.html',{'response':'An error occurred while login please check your credentials.',
                                                  'tab':'credentials error'})
    elif request.method == 'GET':
        return render(request,'404.html',{'response':'404 Not found',
                                          'tab':'Not Found'})
    return HttpResponse("auth endpoint")
    pass

# Unique User


# login url
def ulogin(request):
    return render(request,'registration/login.html',{})
    pass

# logout url
def ulogout(request):
    logout(request)
    return redirect('/')

# cart url
@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Coffee.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Coffee.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Coffee.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Coffee.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart.html')

def about(request):
    return render(request,'about.html',{})

def contact(request):
    return render(request,'contact.html',{})