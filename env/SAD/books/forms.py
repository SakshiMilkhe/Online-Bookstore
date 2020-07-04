from django import forms
from .models import Books

class SearchForm(forms.Form):
    book_search = forms.CharField(label="", max_length=150)

    class Meta:
        fields = ['book_search']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['book_search'].widget.attrs['style'] = 'width:500px; '


class BookUpdate(forms.ModelForm):
    book_name = forms.CharField(max_length=100)
    book_author = forms.CharField(max_length=100)
    book_no = forms.IntegerField()
    book_url = forms.URLField(max_length=250)
    book_genre = forms.CharField(max_length=250)
    rating_1 = forms.IntegerField()
    rating_2 = forms.IntegerField()
    rating_3 = forms.IntegerField()
    rating_4 = forms.IntegerField()
    rating_5 = forms.IntegerField()
    rating_count = forms.IntegerField()
    average_rating = forms.DecimalField(max_digits=5)
    price = forms.IntegerField()

    class Meta:
        model = Books
        fields = ['book_name','book_author','book_no','book_url','book_genre','rating_1','rating_2','rating_3','rating_4','rating_5','rating_count','average_rating','price']