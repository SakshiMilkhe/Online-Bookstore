from django.db import models
from django.contrib.auth.models import User
from books.models import Books
from django.utils import timezone
from django.contrib.auth.models import User

from cities_light.models import Country,City,Region






class WishList(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Address(models.Model):
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.IntegerField()
    contact_no = models.IntegerField()

class Order(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE,default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    address_id = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True,default=None)
    date_of_post = models.DateTimeField(default=timezone.now)
    order_key = models.TextField()
    quantity = models.IntegerField(default=1)
    rating =models.IntegerField(default=0)




class Cart(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)




class tempCart(models.Model):
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)




