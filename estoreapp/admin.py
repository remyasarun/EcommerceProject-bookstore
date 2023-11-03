from django.contrib import admin

from estoreapp.models import Customer, BOOKDETAILS, Cart


# Register your models here.

@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list = ['id', 'Firstname', 'Lastname', 'Email', 'Phone', 'Password']


@admin.register(BOOKDETAILS)
class BOOKDETAILS(admin.ModelAdmin):
    list = ['id', 'Title', 'Author', 'Sellingprice', 'Discountprice', 'Discription', 'Language', 'Product', 'Category', 'Productimage']
    list_filter = ['Category', 'Author','Language']


@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list = ['id', 'Email', 'Product', 'quantity']
    list_filter = ['Email', 'Product']