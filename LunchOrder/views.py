# Create your views here.
from LunchOrder.models import Order,Ingredient,Meal,UserProfile,CATEGORY_CHOICES
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime

#Basic order-page views

def OrderPage(request):
    if not request.user.is_authenticated(): 
        return render_to_response('indexredirect.html', context_instance=RequestContext(request))
    else:
        if request.POST:
            returned = True
        else: 
            returned = False
        ingredientlist = Ingredient.objects.all()
        categories = []
        for categoryref in CATEGORY_CHOICES:
            temporarycategorylist = (categoryref[1],[]) 
            for ingredient in ingredientlist:
                if ingredient.category == categoryref[0]:
                    temporarycategorylist[1].append(ingredient)
            categories.append(temporarycategorylist)
        profile = request.user.get_profile()
        return render_to_response("order.html", {"categories": categories,
                                                 "returned":returned},context_instance=RequestContext(request))
def Confirm(request):
    if not request.user.is_authenticated(): 
        return render_to_response('indexredirect.html', context_instance=RequestContext(request))
    else:
        newmeal = Meal()
        newmeal.save()
        templist = []
        falselist = []
        for ingr in Ingredient.objects.all():
            try:
                added = request.POST[str(ingr.id)]
            except KeyError:
                added = False
                falselist.append(ingr)
            if added:
                newmeal.ingredients.add(ingr)
                templist.append(ingr)
        mealstyle = request.POST["style"]
        pickuptime = request.POST["DOW"]+" - "+request.POST["hour"]+":"+request.POST["minute" ]+" "+request.POST["AMPM"]
        use = request.user
        neworder = Order(style=mealstyle,meal=newmeal,submitted=datetime.datetime.now(),pickup=pickuptime,user=use, confirmed=False, isfilled = False)
        neworder.save() 
        choices = []
        for categoryref in CATEGORY_CHOICES:
            temporarycategorylist = (categoryref[1],[]) 
            for ingredient in neworder.meal.ingredients.all():
                if ingredient.category == categoryref[0]:
                    temporarycategorylist[1].append(ingredient)
            if temporarycategorylist:
                choices.append(temporarycategorylist)
        return render_to_response("submit.html",{"Order":neworder,
                                                 "Choices":choices}, context_instance=RequestContext(request))
def SubmitOrder(request):
    if not request.user.is_authenticated(): 
        return render_to_response('indexredirect.html', context_instance=RequestContext(request))
    else:
        orderid = int(request.POST['OrderId']) 
        order = Order.objects.get(pk=orderid)
        order.confirmed = True
        order.save()
        return render_to_response('submitted.html', context_instance=RequestContext(request))

def Index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def OrdersView(request):
    if not request.user.is_authenticated(): 
        return render_to_response('indexredirect.html', context_instance=RequestContext(request))
    else:
        orderlist = []
        filledlist= []
        for order in Order.objects.all():
            if order.user == request.user:
                if order.confirmed:
                    orderlist.append(order)
        for order in orderlist:
            if order.isfilled:
                orderlist.remove(order)
                filledlist.append(order)
        return render_to_response('ordersview.html', {"Orders":orderlist,
                                                      "FilledOrders":filledlist}, context_instance=RequestContext(request))
#Auth system views

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return render_to_response('index.html', context_instance=RequestContext(request))
    else: 
        return render_to_response('index.html', {'loginerror':True}, context_instance=RequestContext(request))
def Logout(request):
    logout(request)
    return render_to_response('index.html', context_instance=RequestContext(request))

def NewUser(request):
    return render_to_response('newuser.html', context_instance=RequestContext(request))

def CreateUser(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    department = request.POST['department']
    room = request.POST['room']
    user = User.objects.create_user(username, email, password)
    userprofile = UserProfile(user=user,room=room,department=department)
    userprofile.save()
    return render_to_response('indexredirect.html', context_instance=RequestContext(request)) 

#Kitchen-Specific views

def Kitchen(request):
    if request.user.get_profile().iskitchenstaff:
        unfilledlist = []
        for order in Order.objects.all():
            if not order.isfilled:
                unfilledlist.append(order)
        return render_to_response('kitchenindex.html', {"orderlist":unfilledlist}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', context_instance=RequestContext(request)) #returns an error, too, eventually

def OrderDetail(request,order_id):
    choices = []
    order = Order.objects.get(pk=order_id)
    for categoryref in CATEGORY_CHOICES:
       temporarycategorylist = (categoryref[1],[]) 
       for ingredient in order.meal.ingredients.all():
           if ingredient.category == categoryref[0]:
              temporarycategorylist[1].append(ingredient)
       if temporarycategorylist:
           choices.append(temporarycategorylist)
    return render_to_response('detail.html',{"order":order,
                                             "choices":choices}, context_instance=RequestContext(request))

def FillOrder(request,order_id):
    if request.user.get_profile().iskitchenstaff:
        order = Order.objects.get(pk=order_id)
        order.isfilled = True
        order.save()
        return Kitchen(request) 
    else: 
        return render_to_response('index.html', context_instance=RequestContext(request)) #remember to make the error message
