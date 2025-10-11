"""
URL configuration for TastyBite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.home),
   path('open_signin/',views.open_signin , name='open_signin'),
   path('open_signup/' ,views.open_signup,name='open_signup'),
   path('signup/',views.signup ,name ='signup'),
   path('signin/',views.signin,name='signin'),
   path('sigin/add_restarurant',views.addrestaruant,name='sigin/add_restarurant'),
   path('addrestarurant',views.addrestaruants,name="addrestarurant"),
   path('sigin/show_restaruant',views.show_restaruants,name="sigin/show_restaruant"),
   path('open_update_restarunt/<int:restaurant_id>',views.open_update_restaurant,name='open_update_restarunt'),
   path('updateRestaurant/<int:restaurant_id>',views.updateRestaurant,name='updateRestaurant'),
   path('deleteRestaurant/<int:restaurant_id>',views.deleteRestaurant,name='deleteRestaurant'),
path("showmenu/<int:restaurant_id>",views.show_menu,name="showmenu"),
path("openadditem/<int:restaurant_id>",views.openadditem,name="openadditem"),
path("additem/<int:restaurant_id>",views.additem,name="additem"),
path("openupadetitem/<int:item_id>",views.open_Updatemenu,name='openupadetitem'),
path("update_menu/<int:item_id>",views.update_menu,name='update_menu'),
path("deleteitem/<int:item_id>",views.delete_item,name='deleteitem'),
#custmoer
# path("show_restaruantsCustomer",views.show_restaruantsCustomer,name='show_restaruantsCustomer'),
path("showmenucustome/<int:restaurant_id>add/<str:username>",views.show_menuCustomer,name="showmenucustomer"),
path('add_to_cart<int:item_id>/add/<str:username>',views.add_to_cart,name='add_to_cart'),
path('show_cart_page/<str:username>',views.show_cart_page,name="show_cart_page"),
path("checkout/<str:username>",views.checkout,name='checkout'),
path("orders/<str:username>",views.Orders,name='orders')
]
