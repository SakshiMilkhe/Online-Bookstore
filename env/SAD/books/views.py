from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Books
from django.http import HttpResponseRedirect
from .forms import SearchForm,BookUpdate
from django.views.generic import ListView
from django.db.models import Q
from user.forms import CartForm,WishForm
from user.models import Cart,WishList,tempCart
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .filters import BookFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math


def bookfilter(request):
    book_list = Books.objects.all()
    books = BookFilter(request.GET, queryset=book_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(books, 20)
    try:
        book = paginator.page(page)
    except PageNotAnInteger:
        book = paginator.page(1)
    except EmptyPage:
        book = paginator.page(paginator.num_pages)
    context = {'filter': book}
    return render(request, 'books/books_list.html', {'filter': book})



def adminMain(request):
    return render(request, 'books/AdminMain.html')



def adminHome(request):
    book_list = Books.objects.all()[0:20]

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            book_search = form.cleaned_data.get('book_search')

            context = {
                'books': Books.objects.all().filter(Q(book_name__contains=book_search) |
                                                    Q(book_author__contains=book_search) |
                                                    Q(book_genre__contains=book_search), )
            }

            return render(request, 'books/adminSearch.html', context)
    else:
        form = SearchForm()

    context ={
        'books':book_list,
        'form':form,
    }
    return render(request, 'books/adminHome.html',context)
def home(request):
    if request.user.is_superuser:
        return redirect ('book-adminMain')
    else:
        home="Trending Books"
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = SearchForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                book_search = form.cleaned_data.get('book_search')

                books= Books.objects.all().filter(Q(book_name__contains=book_search) |
                                                       Q(book_author__contains=book_search)|
                                                       Q(book_genre__contains=book_search),)
                page = request.GET.get('page', 1)
                paginator = Paginator(books, 20)
                try:
                    book = paginator.page(page)
                except PageNotAnInteger:
                    book = paginator.page(1)
                except EmptyPage:
                    book = paginator.page(paginator.num_pages)
                context = {
                    'books': book,

                }

                # context = {
                #     'books': Books.objects.all().filter(Q(book_name__contains=book_search) |
                #                                         Q(book_author__contains=book_search)|
                #                                         Q(book_genre__contains=book_search),)
                # }

                return render(request, 'books/search.html', context)
        else:
            form = SearchForm()

        book_list= ['Medical Books', 'Test Preparation', 'Biographies & Memoirs',
                     'Religion & Spirituality', 'Arts & Photography', 'Literature & Fiction',
                     'Engineering & Transportation', 'Science & Math',
                     'Christian Books & Bibles', "Children's Books", 'Self-Help', 'Law',
                     'Politics & Social Sciences', 'Health, Fitness & Dieting',
                     'Business & Money', 'Parenting & Relationships', 'Sports & Outdoors',
                     'Computers & Technology', 'Cookbooks, Food & Wine',
                     'Crafts, Hobbies & Home', 'Travel', 'Humor & Entertainment', 'Reference',
                     'Calendars', 'History', 'Comics & Graphic Novels', 'Teen & Young Adult',
                     'Romance', 'Science Fiction & Fantasy', 'Mystery, Thriller & Suspense']

        books = Books.objects.all().filter(average_rating__gt=4.6)
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 20)
        try:
            book = paginator.page(page)
        except PageNotAnInteger:
            book = paginator.page(1)
        except EmptyPage:
            book = paginator.page(paginator.num_pages)
        context = {
            'books': book,
            'form': form,
            'book_list': book_list,
            'home': home
        }
        # context = {
        #     'books': Books.objects.all().filter(average_rating__gt =4.6),
        #     'form':form,
        #     'book_list':book_list,
        #     'home':home
        #
        # }

        return render(request, 'books/home.html',context)
"""
class BookListView(ListView):

    model = Books.objects.all().filter(average_rating__gt =4.6)
    template_name = 'books/home.html' #<app>/<model>_<type>.html
    context_object_name = 'books'
"""

def about(request):

    return render(request, 'books/about.html')

def detail(request,pk):

    if request.method == 'POST':

        c_form = CartForm(request.POST)
        w_form = WishForm(request.POST)

        if "buy" in request.POST:

            if login_required():
                return redirect('login')
            userid = request.POST.get('user2_id')
            user_id = User.objects.get(pk=userid)
            tempCart.objects.all().filter(user_id=user_id).delete()
            temp =tempCart()


            bookid = request.POST.get('book2_id')


            book_id = Books.objects.get(pk=bookid)

            temp.user_id = user_id
            temp.book_id = book_id
            temp.quantity = 1
            temp.save()

            return redirect('{}{}'.format("/user/buyOrder/",userid))


        if c_form.is_valid() and 'cart-form' in request.POST:
            x = c_form.cleaned_data['book_id']
            y = c_form.cleaned_data['user_id']

            user = User.objects.get(id=y)
            book = Books.objects.get(id=x)
            cart = Cart()
            cart.user_id=user
            cart.book_id=book
            cart.save()
            pk1= int(y)
            cart = '/cart/'
            s = '/'

            return redirect('{}{}{}'.format(cart,pk1,s))
        elif w_form.is_valid() and 'wish-form' in request.POST:
            x = w_form.cleaned_data['book_id']
            y = w_form.cleaned_data['user_id']

            user = User.objects.get(id=y)
            book = Books.objects.get(id=x)
            wish = WishList()
            wish.user_id = user
            wish.book_id = book
            wish.save()
            pk1 = int(y)
            wish1 = '/wishlist/'
            wish2='list/'
            s = '/'

            return redirect('{}{}{}{}'.format(wish1,wish2, pk1, s))





        if login_required():
            return redirect('login')


    else:
        c_form = CartForm()

    book = Books.objects.get(pk=pk)
    carts = Cart.objects.all().filter(user_id=request.user.id).values_list('book_id', flat=True)
    if pk in carts:
        active="0"

    else:
        active="1"
    wish = WishList.objects.all().filter(user_id=request.user.id).values_list('book_id', flat=True)
    if pk in wish:
        activewish="0"

    else:
        activewish="1"



    context = {
        'book': Books.objects.get(pk=pk),
        'c_form': c_form,
        'active':active,
        'activewish':activewish
    }



    return render(request, 'books/detail.html',context)

def adminDetail(request,pk):
    if request.method == "POST":
        if "delete" in request.POST:
            Books.objects.all().filter(pk=pk).delete()

            return redirect('book-adminHome')



    context = {
        'book': Books.objects.get(pk=pk),

    }

    return render(request, 'books/adminDetail.html', context)

def filter(request,book):
    book_list = ['Medical Books', 'Test Preparation', 'Biographies & Memoirs',
                 'Religion & Spirituality', 'Arts & Photography', 'Literature & Fiction',
                 'Engineering & Transportation', 'Science & Math',
                 'Christian Books & Bibles', "Children's Books", 'Self-Help', 'Law',
                 'Politics & Social Sciences', 'Health, Fitness & Dieting',
                 'Business & Money', 'Parenting & Relationships', 'Sports & Outdoors',
                 'Computers & Technology', 'Cookbooks, Food & Wine',
                 'Crafts, Hobbies & Home', 'Travel', 'Humor & Entertainment', 'Reference',
                 'Calendars', 'History', 'Comics & Graphic Novels', 'Teen & Young Adult',
                 'Romance', 'Science Fiction & Fantasy', 'Mystery, Thriller & Suspense']

    book=int(book)
    booki = book_list[book-1]



    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            book_search = form.cleaned_data.get('book_search')


            context = {
                'books': Books.objects.all().filter(Q(book_name__contains=book_search) |
                                                    Q(book_author__contains=book_search)|
                                                    Q(book_genre__contains=book_search),),

            }
            return render(request, 'books/search.html', context)
    else:
        form = SearchForm()
        home="Trending Books"



    context = {
        'books': Books.objects.all().filter(book_genre=booki),
        'form':form,
        'book_list': book_list,
        'home':booki





    }


    return render(request,'books/home.html', context)


"""
def ratings(request,rat):
    return render(request, 'books/about.html')

"""

def bookUpdate(request,pk):
    if request.method == 'POST':
        book = Books.objects.get(pk=pk)
        u_form = BookUpdate(request.POST,instance=book)
        if u_form.is_valid():
            u_form.save()

            return redirect('{}{}'.format("/admin/detail/",pk))







    book=Books.objects.get(pk=pk)
    u_form = BookUpdate(instance=book)

    context={
        'u_form':u_form,
        'book':book,
    }

    return render(request, 'books/bookUpdate.html', context)

def userList(request):

    users =User.objects.all()

    context={
        'users':users,
    }

    return render(request, 'books/userList.html', context)
def addBook(request):
    if request.method == 'POST':

        c_form = BookUpdate(request.POST)
        if c_form.is_valid():
            c_form.save()

            return render(request, 'books/about.html')
    else:
        c_form = BookUpdate()

    context={
        'c_form':c_form
    }
    return render(request, 'books/addBook.html', context)