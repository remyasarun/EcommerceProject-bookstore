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
    ('ENGLISH','EN'),
    ('MALAYALAM','ML')
)
STATE_CHOICES = (
    ('AP', 'Andhra Pradesh'),
    ('AS', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CG', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('JK', 'Jammu and Kashmir'),
    ('KA', 'Karnataka'),
    ('Kerala', 'KL'),
    ('LD', 'Lakshadweep'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('PY', 'Puducherry'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TR', 'Tripura'),
    ('TG', 'Telangana'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
)
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending')
)

# Create your models here.
class Customer(models.Model):
    customer_id = models.IntegerField()
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
    Product = models.CharField(max_length=100)
    Category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    Productimage = models.ImageField(upload_to='productimage')
    def __str__(self):
        return self.Title


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(BOOKDETAILS, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s" % (self.user)
    class Meta:
        db_table = "cart"
    @property
    def total_cost(self):
        return self.quantity * self.BOOKDETAILS.Discountprice

class Customerprofile(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=200)
    City = models.CharField(max_length=200)
    Mobile = models.IntegerField(default=0)
    Pincode = models.IntegerField(default=0)
    State = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return "%s " % self.Name

    class Meta:
        db_table = "Customerprofile"
class Payment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customerprofile, on_delete=models.CASCADE)
    product = models.ForeignKey(BOOKDETAILS, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default='')

    @property
    def total_cost(self):
        return self.quantity * self.BOOKDETAILS.Discountprice


class wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(BOOKDETAILS, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.user)



class CODOrderPlaced(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(BOOKDETAILS, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    tracking_no = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='pending')
    payment = models.CharField(max_length=250, null=True)
    paid = models.BooleanField(default=False)

    @property
    def total_cost(self):
        return self.quantity * self.BOOKDETAILS.Discountprice