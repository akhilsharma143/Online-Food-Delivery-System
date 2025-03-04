from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .models import UserSignup
from .models import *
import uuid
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"Index.html")

def restaurants(request):
    restaurants = Restaurant.objects.all()  
    return render(request,"Restaurants.html",{'restaurants':restaurants})

def menu(request):
    main_categories = MainCategory.objects.all()
    return render(request, 'Menu.html', {'main_categories': main_categories})


def cartItem(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer=request.user)
    elif 'user_id' in request.session:
        custom_user_id = request.session['user_id']
        cart_items = Cart.objects.filter(custom_user_id=custom_user_id)
    else:
        return redirect('login')
    total_price = sum(item.product.price for item in cart_items)
    context = {
        'cartItems': cart_items,
        'totalPrice': total_price,
    }
    return render(request, 'cart.html', context)

def additem(request, pid):
    
        product = FoodItem.objects.get(id=pid)
        
        if request.user.is_authenticated:
            Cart.objects.create(product=product, customer=request.user)
        elif 'user_id' in request.session:
            custom_user_id = request.session['user_id']
            custom_user = UserSignup.objects.get(id=custom_user_id)
            Cart.objects.create(product=product, custom_user=custom_user)
        else:
            return redirect('login')
        
        # Add success message
        messages.success(request, f'"{product.name}" has been added to your cart.')

    
        return redirect('menu')


def removeitem(request, pid):
    Cart.objects.filter(id=pid).delete()
    return redirect('cart')

def liked_items(request):
    if request.user.is_authenticated:
        liked_items = LikedItem.objects.filter(customer=request.user)
    elif 'user_id' in request.session:
        custom_user_id = request.session['user_id']
        custom_user = UserSignup.objects.get(id=custom_user_id)
        liked_items = LikedItem.objects.filter(custom_user=custom_user)
    else:
        liked_items = []

    return render(request, 'like.html', {'likedItems': liked_items})

def addlike(request, pid):
    product = FoodItem.objects.get(id=pid)
    
    if request.user.is_authenticated:
        LikedItem.objects.create(product=product, customer=request.user)
    elif 'user_id' in request.session:
        custom_user_id = request.session['user_id']
        custom_user = UserSignup.objects.get(id=custom_user_id)
        LikedItem.objects.create(product=product, custom_user=custom_user)
    else:
        return redirect('login')
    messages.success(request, f'"{product.name}" has been added to your favourites.')
    
    return redirect('menu')

def removelike(request, pid):
    LikedItem.objects.filter(id=pid).delete()
    return redirect('like')

def signup(request):
    if request.method == 'POST':
        Name = request.POST["FirstName"]
        username = request.POST["Username"]
        Lastname = request.POST["LastName"]
        Email = request.POST["Email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        dob = request.POST['dob']
        gender = request.POST['gender']

        obj = UserSignup(
            FirstName=Name,
            LastName=Lastname,
            Username=username,
            Email=Email,
            phone=phone,
            Password=make_password(password),  
            dob=dob,
            gender=gender
        )
        obj.save()
        messages.success(request, f'User "{username}" has been successfully registered!')
        
        return redirect('login')

    return render(request, "signup.html")

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        cuser = UserSignup.objects.filter(Username=username).first()  

        if cuser and check_password(password, cuser.Password):
            
            request.session['user_id'] = cuser.id
            request.session['username'] = cuser.Username
            return redirect('home')  
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user) 
                return redirect('home') 

            return redirect('login')  
    return render(request, 'login.html')

def search(request):
    query = request.GET.get('q')  
    if query:
        results = FoodItem.objects.filter(name__icontains=query)
    else:
        results = FoodItem.objects.none() 

    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'search_results.html', context)

def logoutUser(request):
    request.session.flush() 
    return redirect('login')


def userprofile(request):
    return render(request, "UserProfile.html")

def about(request):
    return render(request, "#about/index.html")


def addAddress(request):
    if request.method == 'POST':
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        address = request.POST["Address"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]

       
        if request.user.is_authenticated:
            user_signup = UserSignup.objects.filter(Username=request.user.username).first()
        elif 'user_id' in request.session:
            custom_user_id = request.session['user_id']
            user_signup = UserSignup.objects.filter(id=custom_user_id).first()
        
        if user_signup:
            # Create a new address associated with the user
            Address.objects.create(
                user=user_signup,
                Name=name,
                Email=email,
                address=address,
                phone=phone,
                city=city,
                state=state,
                pincode=pincode,
                gender=gender,
            )
            return redirect('checkout')
        else:
            return redirect('login')
    
    return redirect('checkout')

def checkout(request):
    user_data = None
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer=request.user)
        user_data = Address.objects.filter(user__Username=request.user.username)
    elif 'user_id' in request.session:
        custom_user_id = request.session['user_id']
        cart_items = Cart.objects.filter(custom_user_id=custom_user_id)
        user_data = Address.objects.filter(user_id=custom_user_id)
    else:
        return redirect('login')

    total_price = sum(item.product.price for item in cart_items)

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        selected_address = Address.objects.get(id=selected_address_id)
        
        order_id = str(uuid.uuid4())[:8]
        
        new_order = Order.objects.create(
            customer=selected_address.user,
            orderId=order_id,
            totalPrice=total_price,
            status='Order placed',
            address=selected_address
        )
        new_order.items.set([item.product for item in cart_items])
        cart_items.delete()

        # Redirect to order confirmation page with order ID
        return redirect('order_confirmation', order_id=order_id)

    context = {
        'cartItems': cart_items,
        'totalPrice': total_price,
        'userData': user_data,
    }
    return render(request, "checkout.html", context)

def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(orderId=order_id)
    except Order.DoesNotExist:
        return render(request, 'order_confirmation.html', {'error': 'Order not found'})

    context = {
        'order': order,
    }
    return render(request, 'order_confirmation.html', context)   

def myaccount(request):
    userData = []
    orderData = []
    if request.user.is_authenticated:
        # Check if the user is an instance of the custom UserSignup model
        if hasattr(request.user, 'usersignup'):
            user = request.user.usersignup  
            userData = Address.objects.filter(user=user)
            orderData = Order.objects.filter(customer=user)
        elif isinstance(request.user, User):
            messages.warning(request, "Admin accounts do not have personal account data.")
    elif 'user_id' in request.session:
        
        custom_user_id = request.session.get('user_id')
        user = UserSignup.objects.filter(id=custom_user_id).first()
        if user:
            userData = Address.objects.filter(user=user)
            orderData = Order.objects.filter(customer=user)
    else:
        messages.warning(request, "Please log in to access your account.")
        return redirect('login')
    
    context = {
        'userData': userData,
        'Orders': orderData,
    }
    return render(request, 'myaccount.html', context)

