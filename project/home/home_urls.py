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
    path('checkout/callback/',views.checkout_callback,name='checkout_callback'),

    # cart url
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    
    
    path('about/',views.about,name='about'),

    path('contact/',views.contact,name='contact')
]
