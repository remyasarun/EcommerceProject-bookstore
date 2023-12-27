from django.contrib import admin

from estoreapp.models import Customer, BOOKDETAILS, Cart, Customerprofile, Payment, OrderPlaced, wishlist, \
    CODOrderPlaced


# Register your models here.

@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list = ['id', 'Firstname', 'Lastname', 'Email', 'Phone', 'Password']


@admin.register(BOOKDETAILS)
class BOOKDETAILS(admin.ModelAdmin):
    list = ['id', 'Title', 'Author', 'Sellingprice', 'Discountprice', 'Discription', 'Language', 'Product', 'Category', 'Productimage']
    list_filter = ['Category', 'Author', 'Language']


@admin.register(Customerprofile)
class Customerprofile(admin.ModelAdmin):
    list = ['user', 'Name', 'Address', 'City', 'Mobile', 'Pincode', 'State']
    list_filter = ['Name']

@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list = ['id', 'user', 'product', 'quantity']

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

@admin.register(OrderPlaced)
class Payment(admin.ModelAdmin):
    list = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']

@admin.register(CODOrderPlaced)
class CODOrderPlaced(admin.ModelAdmin):
    list = ['id', 'user', 'product', 'quantity', 'ordered_date', 'status', 'payment', 'tracking_no', 'status','order_id', 'payment_id', 'amount','paid']


@admin.register(wishlist)
class wishlist(admin.ModelAdmin):
    list = ['id', 'user', 'product']