# Create your views here.
from LunchOrder.models import Order,Ingredient,Meal,User,CATEGORY_CHOICES
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
import datetime

def OrderPage(request):
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
    return render_to_response("order.html", {"categories": categories,
                                             "returned":returned},context_instance=RequestContext(request))

def Confirm(request):
    newmeal = Meal()
    newmeal.save()
    for ingr in Ingredient.objects.all():
        try:
            added = request.POST[ingr.name]
        except KeyError:
            added = False
        if added:
            newmeal.ingredients.add(ingr)
    mealstyle = request.POST["style"]
    pickuptime = request.POST["DOW"]+". - "+request.POST["hour"]+":"+request.POST["minute" ]+" "+request.POST["AMPM"]
    use = User.objects.all()[0] #Just grab the default user. this is a debug measure, get rid of!
    neworder = Order(style=mealstyle,meal=newmeal,submitted=datetime.datetime.now(),pickup=pickuptime,user=use, confirmed=False)
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
    submit = request.POST['Qu']
    orderid = int(request.POST['OrderId']) 
    order = Order.objects.get(pk=orderid)
    order.confirmed = True
    return render_to_response('submitted.html')
