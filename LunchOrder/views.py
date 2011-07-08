# Create your views here.
from LunchOrder.models import Order,Ingredient,Meal,User,CATEGORY_CHOICES
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext

def Order(request):
    ingredientlist = Ingredient.objects.all()
    categories = []
    for categoryref in CATEGORY_CHOICES:
        temporarycategorylist = (categoryref[1],[]) 
        for ingredient in ingredientlist:
	    if ingredient.category == categoryref[0]:
               temporarycategorylist[1].append(ingredient)
        categories.append(temporarycategorylist)
    return render_to_response("order.html", {"categories": categories},context_instance=RequestContext(request))

def SubmitOrder(request):
    Data = request.POST
    #Go through the post data, get rid of the csrf stuff, put the time and type info in one var
    #put the ingredients in another, organised by category. 
    return render_to_response("submit.html",{"data": Data}, context_instance=RequestContext(request))
