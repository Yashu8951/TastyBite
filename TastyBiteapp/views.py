from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Customer
from .models import Restaurant,Item,Cart
from django.contrib import messages 
import razorpay
from django.conf import settings

def home(request):
    return render(request,'html/home.html')
# Create your views here.

def open_signin(request):
    return render(request,'html/Login.html')

def open_signup(request):
    return render(request,'html/Register.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        try:
            if Customer.objects.get(username =username):
                return HttpResponse("Not allowed")
            else:
                Customer.objects.create(username = username,
                                password = password,
                                email=email,
                                mobile =mobile,
                                address = address)
            return render(request,'html/Login.html')
        except :
            HttpResponse("Internal server error")

def signin(request):
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get("password")
    try:
        Customer.objects.filter(username =username,password=password)
        if username == "Admin":
            return render(request,"html/Admin.html")
        else:
            restaurant =Restaurant.objects.all()
            return render(request,"html/Customer.html",{"restaurant":restaurant,'username':username})
    except Customer.DoesNotExist:
            return render(request, 'delivery/fail.html')
            return HttpResponse("Invalid request")   

def addrestaruant(request):
    return render(request,'html\Add_restarurant.html')


def addrestaruants(request):
 if request.method == 'POST':
     name = request.POST.get("name")
     picture = request.POST.get("picture")
     cuisine = request.POST.get("cuisine")
     rating = request .POST.get("rating")
     Restaurant.objects.create(name =name,
                               picture = picture,
                               cuisine =cuisine,
                               rating =rating)
     restaurant = Restaurant.objects.all();
     return render(request,'html/show_restarurant.html',{'restaurant': restaurant})
 
def show_restaruants(request):
    restaurant = Restaurant.objects.all();
    return render(request,'html/show_restarurant.html',{'restaurant': restaurant})

def open_update_restaurant(request ,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)
    return render(request,"html/updateRestaurant.html",{"restaurant":restaurant })

def updateRestaurant(request ,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)
    restaurant.name = request.POST.get("name")
    restaurant.picture = request.POST.get("picture")
    restaurant.cuisine = request.POST.get("cuisine")
    restaurant.rating = request.POST.get("rating")
    restaurant.save()
    return redirect('sigin/show_restaruant')

def deleteRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.delete()
        # Redirect to the restaurant list page after deletion
        return redirect('sigin/show_restaruant')  # Use the name of your list view

    # For GET requests, either redirect or show a confirmation
    return redirect('sigin/show_restaruant')
    
def show_menu(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)
    item= Item.objects.filter(restaurant=restaurant)
    return render(request,"html/showmenu.html",{'restaurant': restaurant,'item':item})

def openadditem(request,restaurant_id):
    restaurant =get_object_or_404(Restaurant,id=restaurant_id)
    return render(request,"html/open_additem.html",{'restaurant': restaurant})

def additem(request,restaurant_id):
      restaurant = get_object_or_404(Restaurant,id=restaurant_id)

      if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return redirect('showmenu' ,restaurant_id =restaurant.id)

def open_Updatemenu(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, "html/update_menuitems.html", {"items": item})

def update_menu(request, item_id):
    menuItem = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        menuItem.name = request.POST.get('name')
        menuItem.description = request.POST.get('description')
        menuItem.price = request.POST.get('price')
        menuItem.is_veg = 'is_veg' in request.POST
        menuItem.picture = request.POST.get("picture")
        menuItem.save()
       
        return redirect('showmenu', restaurant_id=menuItem.restaurant.id)
    
def delete_item(request,item_id):
    item = get_object_or_404(Item,id=item_id)
    item.delete()
    return redirect("showmenu",restaurant_id=item.restaurant.id)

# custmoer 
# def show_restaruantsCustomer(request):
#     restaurant = Restaurant.objects.all();
#     customer =Customer.objects.all()
#     return render(request,'html/Customer.html',{'restaurant': restaurant})


def show_menuCustomer(request,restaurant_id,username):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)
    item= Item.objects.filter(restaurant=restaurant)
    return render(request,"html/showmenucustomer.html",{'restaurant': restaurant,'item':item,"username":username})


def add_to_cart(request,item_id,username):
    customer = get_object_or_404(Customer,username=username)
    item = get_object_or_404(Item,id=item_id)

    cart ,created = Cart.objects.get_or_create(customer=customer)

    cart.items.add(item)
    messages.success(request,f"{item.name} added to your cart!")
    return redirect('showmenucustomer', restaurant_id=item.restaurant.id, username=username)
    

def show_cart_page(request,username):
     customer = get_object_or_404(Customer,username=username)
     cart = Cart.objects.filter(customer=customer).first()

     item = cart.items.all() if cart else []
     total_price = cart.total_price if cart else 0

     return render(request , "html/cart.html", {
         'items':item,
         'total_price':total_price,
         'username':username
     })

def checkout(request, username):
    customer = get_object_or_404(Customer,username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price if cart else 0


    if total_price == 0:
        return render(request ,"html/checkout.html",{
            'error' :"your is empty"

        })
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    return render(request, 'html/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })


def Orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()  # Get a single cart

    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price if cart else 0  # total_price is a property, not method

    if cart:
        cart.items.clear()  # Clear items after placing order

    return render(request, 'html/orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })
