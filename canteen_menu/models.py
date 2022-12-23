from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from my_user.models import Profile


class Canteen(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length = 200)  # Name of the food item
    price = models.IntegerField(default = 0)   # Price of the food item
    cooked_in = models.ForeignKey("Canteen", on_delete = models.CASCADE)  # Canteen in which the food item can be found

    def __str__(self):
        return f"{self.name} of {self.cooked_in.__str__()} (Rs{self.price})"

class Due(models.Model):
    person = models.ForeignKey("my_user.Profile", on_delete=models.CASCADE)  # Name of the person who owes the money
    canteen = models.ForeignKey("Canteen", on_delete=models.CASCADE)  # Canteen in which the food item was bought
    amount = models.IntegerField(default = 0)  # Amount of money owed
    date = models.DateField(default = now)  # Date on which the money was owed

    def __str__(self):
        return f"{self.person.user.name} owes Rs{self.amount} to {self.canteen.name} on {self.date.strftime('%a, %d %b %Y')}."

    def name(self):
        return self.__str__()