from django.db import models

# Create your models here

class User(models.Model):
	#User Info- need to get OpenId thing in here...
	Department = models.CharField(max_length = 20)
 
class Order(models.Model):
	User = models.ForeignKey("LunchOrder.User")
	Meal = models.ForeignKey("LunchOrder.Meal")

class Meal(models.Model):
	Name = models.CharField(max_length = 20)
	
