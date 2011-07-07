from django.db import models

# Create your models here

class User(models.Model):
    #User Info- need to get OpenId thing in here...
    department = models.CharField(max_length = 20)
    room = models.CharField(max_length = 4) 
class Order(models.Model):
    user = models.ForeignKey(User)
    meal = models.ForeignKey(Meal)

class Meal(models.Model):
    ingredients = models.ManyToManyField(Ingredient)

class Ingredient(models.Model):
    name = models.CharField(max_length = 20)  
	
