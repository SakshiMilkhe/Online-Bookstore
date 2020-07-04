from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cart,WishList
from cities_light.models import Region,City


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class CartForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:

        fields = ['book_id','user_id']

class WishForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:

        fields = ['book_id','user_id']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']


cities = tuple(City.objects.values_list('id','name'))
region = tuple(Region.objects.values_list('id','name'))


class AddressUpdateForm(forms.ModelForm):

    region = forms.CharField(widget=forms.Select(choices=region))
    city = forms.CharField(widget=forms.Select(choices=cities))
    address = forms.CharField()
    pincode = forms.IntegerField()
    contact_no = forms.IntegerField()
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = City
        fields = ['region','city','address','pincode','contact_no']

class DeleteFromCart(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model =Cart
        fields = ['book_id', 'user_id']

class DeleteFromWishList(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model =WishList
        fields = ['book_id', 'user_id']


