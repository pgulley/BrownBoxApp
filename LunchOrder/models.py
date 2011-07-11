from django.db import models

# Create your models here

class User(models.Model):
    #User Info- need to get OpenId thing in here...
    department = models.CharField(max_length = 20)
    room = models.CharField(max_length = 4) 

CATEGORY_CHOICES =( 
('M', 'Main'),
('V', 'Veggie'),
('C', 'Condiments'),
('WS', 'Weekly Special'),
('CH', 'Cheeses'),
('D', 'Dressings'),
('CO', 'Cookies'),
)
class Ingredient(models.Model):
    name = models.CharField(max_length = 20)  
    category = models.CharField(choices=CATEGORY_CHOICES, max_length = 2)
    def __unicode__(self): 
        return "{0} : {1}".format(self.category,self.name)
class Meal(models.Model):
    ingredients = models.ManyToManyField("Ingredient")
class Order(models.Model):
    STYLE_CHOICES =( 
('R', 'Roll'),
('W', 'Wrap'),
('S', 'Salad'),
)
    DAY_CHOICES =( 
('Tue', 'Tuesday'),
('Thurs', 'Thursday'),
)
    user = models.ForeignKey(User)
    meal = models.ForeignKey(Meal)
    style = models.CharField(max_length=1,choices=STYLE_CHOICES)
    submitted = models.DateTimeField()
    pickup = models.CharField(max_length=10)
    confirmed = models.BooleanField()
