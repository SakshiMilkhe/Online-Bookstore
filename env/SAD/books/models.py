from django.db import models

class Books(models.Model):
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    book_no = models.IntegerField()
    book_url = models.URLField(max_length=250)
    book_genre = models.CharField(max_length=250)
    rating_1 = models.IntegerField()
    rating_2 = models.IntegerField()
    rating_3 = models.IntegerField()
    rating_4 = models.IntegerField()
    rating_5 = models.IntegerField(default=0)
    rating_count = models.IntegerField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.IntegerField()



    def __str__(self):
        return self.book_name





