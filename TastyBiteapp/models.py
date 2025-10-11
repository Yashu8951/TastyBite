from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=20)

class Restaurant(models.Model):
     name = models.CharField(max_length=20)
     picture = models.CharField(max_length=200,default="")
     cuisine = models.CharField(max_length=200)
     rating =models.FloatField()


class Item(models.Model):
     restaurant= models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="items")
     name = models.CharField(max_length=20)
     picture=models.CharField(max_length=200)
     description =models.CharField(max_length=200)
     price =models.FloatField()
     is_veg = models.BooleanField(default=True)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField("Item", related_name="cart")

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"{self.customer.username} - Total: {self.total_price}"


