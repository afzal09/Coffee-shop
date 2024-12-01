from django.urls import path

from . import views

urlpatterns = [
    # root url
    path('',views.index,name='index'),

    # signup urls
    path('accounts/signup/',views.signup,name='signup'),    
    path('accounts/signup/auth/',views.auth,name='auth'),

    # login urls
    path('accounts/login/',views.ulogin,name='login'),
    path('accounts/login/auth/',views.auth,name='auth'),

    # logout urls
    path('accounts/logout/',views.ulogout,name='logout'),

    # shop url
    path('shop/',views.shop,name='shop'),

    # order url
    path('order/<int:id>/',views.order,name='order'),

    # chechout url
    path('checkout/',views.checkout,name='checkout'),

    # cart url
    path('my_orders/',views.my_orders,name='my_orders'),
    
    
    path('about/',views.about,name='about'),

    path('contact/',views.contact,name='contact')
]