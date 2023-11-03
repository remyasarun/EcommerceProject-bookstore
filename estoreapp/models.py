from django.db import models

CATEGORY_CHOICES = (
    ('NV', 'NOVELS'),
    ('PT', 'POETRY'),
    ('SR', 'STORY'),
    ('CD', 'CHILDRENS'),
    ('SC', 'SCIENCE'),
    ('AT', 'AUTOBIOGRAPHY'),
)
LANGUAGE_CHOICES = (
    ('EN', 'ENGLISH'),
    ('ML', 'MALAYALAM')
)

# Create your models here.
class Customer(models.Model):
    First_name = models.CharField(max_length=10)
    Last_name = models.CharField(max_length=10)
    Email = models.EmailField(max_length=20, unique=True)
    Phone = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s" % (self.First_name, self.Last_name)

    class Meta:
        db_table = "customerdetails"


class BOOKDETAILS(models.Model):
    Title = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    Sellingprice = models.IntegerField(default=0)
    Discountprice = models.IntegerField(default=0)
    Discription = models.TextField(max_length=1000)
    Language = models.CharField(choices=LANGUAGE_CHOICES, max_length=100)
    Product = models.CharField( max_length=100)
    Category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    Productimage = models.ImageField(upload_to='productimage')
    def __str__(self):
        return self.Title


class Cart(models.Model):
    Email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Product = models.ForeignKey(BOOKDETAILS, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s" % (self.Email)
    class Meta:
        db_table = "cart"