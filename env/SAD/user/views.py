from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserUpdateForm,AddressUpdateForm,DeleteFromCart,WishForm,DeleteFromWishList
from django.contrib import messages
from .forms import CartForm
from .models import Cart as Kart
from .models import WishList,Order,tempCart
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cities_light.models import Region,City
from .models import Address
from books.models import Books
from django.core.mail import send_mail
import itertools
import numpy as np
import random
from django.conf import settings
from django.http import HttpResponse
import datetime
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf




def register(request):
    if request.method == 'POST':
        form =  UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'The user {username} is successfully created!')
            # subject = 'Thank you for registering to our site'
            # message = ' it  means a world to us '
            # emailAdd = form.cleaned_data['email']
            # print(emailAdd)
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [emailAdd]
            #
            # send_mail(subject, message, email_from, recipient_list)
            return redirect('login')

    else:
        form =  UserRegisterForm()
    return render(request, 'user/register.html',context={'form':form})

@login_required
def Cart(request,pk):
    isMore=0

    if request.method == 'POST':

        if "decrement" in request.POST:
            bookNum = int(request.POST.get('bookNum'))


            cart = Kart.objects.get(pk=bookNum)
            if cart.quantity!=1:
                cart.quantity=cart.quantity-1
                cart.save()

        if "increment" in request.POST:

            bookNum = int(request.POST.get('bookNum'))


            print("incrementeddddd")
            cart = Kart.objects.get(pk=bookNum)
            if cart.quantity ==3:
                isMore=isMore+1
            else:
                cart.quantity=cart.quantity+1
                cart.save()


    user = User.objects.get(id=pk)

    cart = Kart.objects.all().filter(user_id=user)
    sum = 0
    qty = 0
    for book in cart:
        if book.quantity>1:
            sum = sum + book.quantity*book.book_id.price
            qty = qty + book.quantity
        else:
            sum = sum + book.book_id.price
            qty = qty + 1

    if request.method =='POST':

        form = DeleteFromCart(request.POST)

        if form.is_valid():
            x = form.cleaned_data['book_id']
            y = form.cleaned_data['user_id']
            user = User.objects.get(id=y)
            book = Books.objects.get(id=x)
            Kart.objects.all().filter(user_id=user).filter(book_id=book).delete()
            pk1 = int(y)
            cart = '/cart/'
            s = '/'

            return redirect('{}{}{}'.format(cart, pk1, s))


    else:
        form=DeleteFromCart()

    print("yyyyyyyyyyyyyyy",type(cart))

    if isMore>0:
        messages.warning(request,
                         f'You cannot Add more than 3 books. Please create another order if you want to do so.')
        context = {
            'cart': cart,
            'sum': sum,
            'qty': qty,
            'form':form,
            'q':"ho",
        }
    else:
        context = {
            'cart': cart,
            'sum': sum,
            'qty': qty,
            'form': form,
            'q': "ho",
        }

    return render(request, 'user/cart.html', context)

@login_required
def wishList(request,pk):
    user = User.objects.get(id=pk)

    wishlist = WishList.objects.all().filter(user_id=user)

    if request.method =='POST':

        form = DeleteFromWishList(request.POST)

        if form.is_valid():
            x = form.cleaned_data['book_id']
            y = form.cleaned_data['user_id']
            user = User.objects.get(id=y)
            book = Books.objects.get(id=x)
            WishList.objects.all().filter(user_id=user).filter(book_id=book).delete()
            pk1 = int(y)
            wish1 = '/wishlist/'
            wish2 = 'list/'
            s = '/'

            return redirect('{}{}{}{}'.format(wish1, wish2, pk1, s))
            #return redirect('{}{}{}'.format("/book/", "detail/", x))




    else:
        form=DeleteFromWishList()

    context = {
        'wishlist':wishlist,
        'form': form,
    }






    return render(request, 'user/wishList.html', context)





def address_create(request):


    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AddressUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid() and a_form.is_valid():
            """print(a_form.cleaned_data['region'])
            print(a_form.cleaned_data['city'])
            print(a_form.cleaned_data['address'])
            print(a_form.cleaned_data['pincode'])
            print(a_form.cleaned_data['contact_no'])
            print(a_form.cleaned_data['user_id'])
            """
            region = a_form.cleaned_data['region']
            city = a_form.cleaned_data['city']
            address = a_form.cleaned_data['address']
            pincode = a_form.cleaned_data['pincode']
            contact = a_form.cleaned_data['contact_no']
            user = a_form.cleaned_data['user_id']

            region_id = Region.objects.get(id=region)
            city_id = City.objects.get(id=city)
            user_id = User.objects.get(id=user)

            add = Address()
            add.region_id =region_id
            add.city_id = city_id
            add.user_id = user_id
            add.address = address
            add.contact_no = contact
            add.pincode  = pincode

            add.save()


            messages.success(request, f'The User Address is Added')
            return redirect('user-address')

    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AddressUpdateForm(instance=request.user)


    context = {

        'u_form': u_form,
        'a_form': a_form,

    }

    return render(request,'user/addressCreate.html',context)
def address(request):


    """if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AddressUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid() and a_form.is_valid():
            print(a_form.cleaned_data['region'])
            print(a_form.cleaned_data['city'])
            print(a_form.cleaned_data['address'])
            print(a_form.cleaned_data['pincode'])
            print(a_form.cleaned_data['contact_no'])
            print(a_form.cleaned_data['user_id'])

            region = a_form.cleaned_data['region']
            city = a_form.cleaned_data['city']
            address = a_form.cleaned_data['address']
            pincode = a_form.cleaned_data['pincode']
            contact = a_form.cleaned_data['contact_no']
            user = a_form.cleaned_data['user_id']

            region_id = Region.objects.get(id=region)
            city_id = City.objects.get(id=city)
            user_id = User.objects.get(id=user)

            add = Address()
            add.region_id =region_id
            add.city_id = city_id
            add.user_id = user_id
            add.address = address
            add.contact_no = contact
            add.pincode  = pincode

            add.save()


            messages.success(request, f'The User Address is Added')
            return redirect('user-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AddressUpdateForm(instance=request.user)
    """
    user = request.user
    count = Address.objects.all().filter(user_id=user).count()
    context = {
        'count': count,
        'address' : Address.objects.all().filter(user_id=user)
    }

    return render(request,'user/address.html',context)

def address_update(request,pk):

    add_inst = Address.objects.get(id=pk)
    if request.method == 'POST':

        a_form = AddressUpdateForm(request.POST,instance=request.user)
        if a_form.is_valid():
            """print(a_form.cleaned_data['region'])
            print(a_form.cleaned_data['city'])
            print(a_form.cleaned_data['address'])
            print(a_form.cleaned_data['pincode'])
            print(a_form.cleaned_data['contact_no'])
            print(a_form.cleaned_data['user_id'])
            """
            region = a_form.cleaned_data['region']
            city = a_form.cleaned_data['city']
            address = a_form.cleaned_data['address']
            pincode = a_form.cleaned_data['pincode']
            contact = a_form.cleaned_data['contact_no']
            user = a_form.cleaned_data['user_id']

            region_id = Region.objects.get(id=region)
            city_id = City.objects.get(id=city)
            user_id = User.objects.get(id=user)

            add = Address(id=pk)
            add.region_id =region_id
            add.city_id = city_id
            add.user_id = user_id
            add.address = address
            add.contact_no = contact
            add.pincode  = pincode

            add.save()



            return redirect('user-address')

    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AddressUpdateForm(instance=add_inst)


    context = {
        'u_form': u_form,
        'a_form': a_form,
    }

    return render(request,'user/addressUpdate.html',context)


def address_delete(request,pk):
    Address.objects.get(id=pk).delete()
    messages.success(request, f'The user Address is Deleted')
    return redirect('user-address')




def profile(request):
    user = request.user
    user_id = user.id

    """address = Address.objects.all().filter(user_id=user)
    count =  Address.objects.all().filter(user_id=user).count()
    context ={
        'address':address,
        'count': count
    }"""

    return render(request, 'user/profile.html')

def order(request,pk):
    if request.method == "POST":
        if "order" in request.POST:
            user = User.objects.get(id=pk)
            cart = Kart.objects.all().filter(user_id=user)
            add=request.POST.get('add')
            address=Address.objects.get(pk=add)
            Randnumber= random.randint(0, 999999)
            key="order-"+ str(Randnumber)
            for c in cart:
                order = Order()
                order.user_id=user
                order.book_id=c.book_id
                order.quantity=c.quantity
                book=Books.objects.get(pk=c.book_id.id)
                book.book_no=book.book_no-c.quantity
                book.save()
                order.order_key=key
                order.address_id=address
                order.save()
                Kart.objects.get(id=c.id).delete()

            return redirect('{}{}'.format("/user/order/list/", pk, ))



    user = User.objects.get(id=pk)
    add_inst = Address.objects.all().filter(user_id=user)
    cart = Kart.objects.all().filter(user_id=user)
    sum1 = 0
    qty = 0
    for book in cart:
        if book.quantity > 1:
            sum1 = sum1 + book.quantity * book.book_id.price
            qty = qty + book.quantity
        else:
            sum1 = sum1 + book.book_id.price
            qty = qty + 1

    context = {
        'address':add_inst,
        'cart':cart,
        'sum':sum1,
        "qty":qty,
    }


    return render(request,'user/order.html',context)

def orderList(request,pk):
    """order = Order.objects.values_list('order_key')
    order1 = list(itertools.chain(*order))
    uniod = np.array(order1)
    uniqueOrder=np.unique(uniod)
    listOrder= Order.values()"""
    if request.method == "POST":
        if "Submit" in request.POST:

            orderKey = request.POST.get('orderKey')
            orders = Order.objects.all().filter(order_key=orderKey)
            orderDate=orders[0].date_of_post
            address=orders[0].address_id
            price=0
            for order in orders:
                price= price +order.book_id.price*order.quantity

            context={
                'orders':orders,
                'orderKey':orderKey,
                'orderDate':orderDate,
                'address':address,
                'user':orders[0].user_id,
                'price':price
            }

            pdf = render_to_pdf('user/invoice.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

    user = User.objects.all().get(id=pk)




    if request.user.is_superuser:
        admin =1
    else:
        admin=0

    context = {
        'admin':admin,
        'order': Order.objects.all().filter(user_id=user).order_by('-date_of_post')
    }
    return render(request, 'user/orderDetails.html', context)


def rate(request, pk):


    if request.method =="POST":
        print("hi")

        if "Submit" in request.POST:

            rating = request.POST.get('rating')
            rating=int(rating)
            order = Order.objects.get(pk=pk)
            order.rating = rating
            order.save()
            return redirect('user-orderReviewed')





    pk=int(pk)
    order = Order.objects.get(pk=pk)
    book = order.book_id
    rat = order.rating
    context={
        'book': book,
        'pk': pk,
        'rat': rat
    }
    return render(request, 'user/rate.html', context)


def orderReviewed(request):

    return render(request, 'user/orderReviewed.html')



def buyOrder(request,pk):
    if request.method == "POST":
        if "order" in request.POST:
            user = User.objects.get(id=pk)
            cart = tempCart.objects.all().filter(user_id=user)
            add=request.POST.get('add')
            address=Address.objects.get(pk=add)
            Randnumber= random.randint(0, 999999)
            key="order-"+ str(Randnumber)
            for c in cart:
                order = Order()
                order.user_id=user
                order.book_id=c.book_id
                order.quantity=c.quantity
                book=Books.objects.get(pk=c.book_id.id)
                book.book_no=book.book_no-c.quantity
                book.save()
                order.order_key=key
                order.address_id=address
                order.save()
                tempCart.objects.get(id=c.id).delete()

            return redirect('{}{}'.format("/user/order/list/", pk, ))



    user = User.objects.get(id=pk)
    add_inst = Address.objects.all().filter(user_id=user)
    cart = tempCart.objects.all().filter(user_id=user)
    sum1 = 0
    qty = 0
    for book in cart:
        if book.quantity > 1:
            sum1 = sum1 + book.quantity * book.book_id.price
            qty = qty + book.quantity
        else:
            sum1 = sum1 + book.book_id.price
            qty = qty + 1

    context = {
        'address':add_inst,
        'cart':cart,
        'sum':sum1,
        "qty":qty,
    }


    return render(request,'user/buyOrder.html',context)











