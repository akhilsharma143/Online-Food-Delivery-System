from django.urls import path
from  .views import *
urlpatterns = [
    path('home/',home,name='home'),
    path('restaurants/',restaurants,name='restaurants'),
    path('cart/',cartItem,name='cart'),
    path('additem/<int:pid>',additem,name='add item'),
    path('removeitem/<int:pid>',removeitem,name='remove item'),
    path('like/',liked_items, name='like'),
    path('add_like/<int:pid>/',addlike, name='add_like'),
    path('remove_like/<int:pid>/',removelike, name='remove_like'),
    path('signup/',signup,name='signup'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('checkout/',checkout,name='checkout'),
    path('order_confirmation/<str:order_id>/',order_confirmation, name='order_confirmation'),
    path('addAddress',addAddress,name='addAddress'),
    path('search/',search, name='search'),
    path('menu/',menu,name='menu'),
    path('myaccount/',myaccount,name='myaccount'),
    path('about/',about,name='about'),
    
]
