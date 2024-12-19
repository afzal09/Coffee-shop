from .models import Coffee , Orders
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    
    context = {

    }
    return render(request, 'checkout/checkout.html', context)
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

# my_orders url
@login_required()
def my_orders(request):
    context = {
        'orders': Orders.objects.all()
    }
    return render(request,'my_orders/my_orders.html',context)

def about(request):
    return render(request,'about.html',{})

def contact(request):
    return render(request,'contact.html',{})