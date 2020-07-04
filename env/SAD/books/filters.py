from .models import Books
import django_filters

class BookFilter(django_filters.FilterSet):

    class Meta:
        model = Books
        fields = ['book_genre', 'price', ]