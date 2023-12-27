import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
import random

from estoreapp.forms import CustomerprofileForm
from estoreapp.models import Customer, BOOKDETAILS, Cart, Customerprofile, wishlist, Payment, OrderPlaced, CODOrderPlaced


# Create your views here.
def Home(request):
    totalitem = 0
    logindata = Customer.objects.get(Email=request.session['email'])
    totalitem = len(Cart.objects.filter(user=logindata))
    return render(request, 'home.html',locals())
def Base(request):
    totalitem = 0
    logindata = Customer.objects.get(Email=request.session['email'])
    totalitem = len(Cart.objects.filter(user=logindata))
    return render(request, 'base.html',locals())
def Footer(request):
    return render(request, 'footer.html')


def Register(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if Customer.objects.filter(Email=email).first():
            messages.error(request, "email id already exist", extra_tags='email')
        elif pass1 == pass2:
            Customer(First_name=first, Last_name=last, Email=email, Phone=phone, password=pass1).save()
            messages.success(request, "Congratulations,User Registered Successfully", extra_tags='done')
            return redirect('/login')

        else:
            messages.error(request, "Password is Not Matching.please re-enter your password", extra_tags='password')

    return render(request, 'register.html')


def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        username = Customer.objects.filter(Email=email, password=pass1)
        print(username)
        if username:
            request.session['email'] = email
            return render(request, 'home.html')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def Logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('login.html')

@method_decorator(login_required, name='dispatch')
class Category(View):
    def get(self, request, val):
        book = BOOKDETAILS.objects.filter(Category=val)
        title = book.filter(Category=val).values('Title')
        totalitem = 0
        logindata = Customer.objects.get(Email=request.session['email'])
        totalitem = len(Cart.objects.filter(user=logindata))
        return render(request, 'category.html', locals())
@method_decorator(login_required, name='dispatch')
class Productdetails(View):
    def get(self, request, pk):
        book = BOOKDETAILS.objects.get(pk=pk)
        totalitem = 0
        logindata = Customer.objects.get(Email=request.session['email'])
        totalitem = len(Cart.objects.filter(user=logindata))
        return render(request, 'productdetails.html', locals())
@method_decorator(login_required, name='dispatch')
class Buynow(View):
    def get(self, request, pk):
        book = BOOKDETAILS.objects.get(pk=pk)
        return redirect('/cart', locals())

@login_required
def addtocart(request):
    if request.method == "POST":
        if 'email' in request.session:
            logindata = Customer.objects.get(Email=request.session['email'])
            print(logindata)
            product_id = request.POST.get('prod_id')
            print(product_id)
            product = BOOKDETAILS.objects.get(id=product_id)
            print(product)
            Cart(user=logindata, product=product).save()
            totalitem = 0
            totalitem = len(Cart.objects.filter(user=logindata))
        return redirect('/cart', locals())

@login_required
def Showcart(request):
    logindata = Customer.objects.get(Email=request.session['email'])
    cart = Cart.objects.filter(user=logindata)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.Discountprice
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=logindata))
    return render(request, 'addtocart.html', locals())

@login_required
def remove_cart(request,id):
    if request.method == 'GET':
        logindata = Customer.objects.get(Email=request.session['email'])
        c = Cart.objects.get(id=id)
        c.delete()
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=logindata))
        return redirect('/cart', {'cart': c}, locals())

@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        form = CustomerprofileForm()
        return render(request, 'profile.html', locals())
    def post(self,request):
        form = CustomerprofileForm(request.POST)
        logindata = Customer.objects.get(Email=request.session['email'])
        if form.is_valid:
            user = logindata
            Name = form.data['Name']
            Address = form.data['Address']
            City = form.data['City']
            Mobile = form.data['Mobile']
            Pincode = form.data['Pincode']
            State = form.data['State']
            Customerprofile(user=user, Name=Name, Address=Address, City=City, Mobile=Mobile, Pincode=Pincode, State=State).save()
            messages.success(request, 'profile saved successfully')
        else:
            messages.error(request, 'something went wrong')
        return render(request, 'profile.html', locals())

@login_required
def address(request):
    user = Customer.objects.get(Email=request.session['email'])
    add = Customerprofile.objects.filter(user=user)
    return render(request, 'address.html', locals())

@method_decorator(login_required, name='dispatch')
class updateaddress(View):
    def get(self, request, pk):
        add = Customerprofile.objects.get(pk=pk)
        form = CustomerprofileForm(instance=add)
        return render(request, 'updateaddress.html', locals())
    def post(self, request, pk):
        form = CustomerprofileForm(request.POST)
        if form.is_valid:
            add = Customerprofile.objects.get(pk=pk)
            add.Name = form.data['Name']
            add.Address = form.data['Address']
            add.City = form.data['City']
            add.Mobile = form.data['Mobile']
            add.Pincode = form.data['Pincode']
            add.State = form.data['State']
            add.save()
            messages.success(request, 'profile updated successfully')
        else:
            messages.error(request, 'something went wrong')
        return render(request, 'updateaddress.html', locals())

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        print(search_query)
        filtered_model = BOOKDETAILS.objects.filter(Product=search_query)
        author_model = BOOKDETAILS.objects.filter(Author=search_query)
        print(filtered_model)
        return render(request, 'search.html', {'search_query': search_query, 'filtered_model': filtered_model, 'author_model':author_model})

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        logindata = Customer.objects.get(Email=request.session['email'])
        cart_item = Cart.objects.filter(user=logindata)
        add = Customerprofile.objects.filter(user=logindata)
        book = BOOKDETAILS.objects.all()
        amount = 0
        for p in cart_item:
            value = p.quantity * p.product.Discountprice
            amount = amount + value
        totalamount = amount + 40
        razoramount = int(totalamount*100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {'amount': razoramount, 'currency': 'INR', 'receipt': 'order_rcptid_12'}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_N0C1AQQLEJesOu', 'entity': 'order', 'amount': 36000, 'amount_paid': 0, 'amount_due': 36000,
        #  'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1699929716}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(user=logindata, amount=totalamount, razorpay_order_id=order_id, razorpay_payment_status=order_status)
            payment.save()
        return render(request, 'checkoutpage.html', locals())

def paymentdone(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    logindata = Customer.objects.get(Email=request.session['email'])
    customer = Customerprofile.objects.filter(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_status = payment_id
    payment.save()
    cart=Cart.objects.filter(user=logindata)
    for c in cart:
        OrderPlaced(user=logindata, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect('/orders')

@login_required
def orders(request):
    logindata = Customer.objects.get(Email=request.session['email'])
    Orderplaced = OrderPlaced.objects.filter(user=logindata)
    CODOrderplaced = CODOrderPlaced.objects.filter(user=logindata)
    return render(request, 'orders.html', locals())
@login_required
def COD(request):
    if request.method == "POST":
        logindata = Customer.objects.get(Email=request.session['email'])
        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        cart_item = Cart.objects.filter(user=logindata)
        amount = 0
        for p in cart_item:
            value = p.quantity * p.product.Discountprice
            amount = amount + value
            totalamount = amount + 40
            trackno = 'BOOKMART' + str(random.randint(1111111, 9999999))
            CODOrderPlaced(user=logindata, product=p.product, amount=totalamount, quantity=p.quantity, tracking_no=trackno, payment_id=payment_id, order_id=order_id).save()
            p.delete()
            return redirect('/orders')

@login_required
def Wishlist(request):
    if request.method == "POST":
        if 'email' in request.session:
            logindata = Customer.objects.get(Email=request.session['email'])
            print(logindata)
            product_id = request.POST.get('prod_id')
            print(product_id)
            product = BOOKDETAILS.objects.get(id=product_id)
            print(product)
            wish = wishlist(user=logindata, product=product)
            wish.save()
            totalitem = 0
            totalitem = len(Cart.objects.filter(user=logindata))
        return redirect('/showwishlist', locals())
@login_required
def Show_wishlist(request):
    logindata = Customer.objects.get(Email=request.session['email'])
    product = wishlist.objects.filter(user=logindata)
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=logindata))
    return render(request, 'wishlist.html', locals())
@login_required
def remove_wishlist(request,id):
    if request.method == 'GET':
        logindata = Customer.objects.get(Email=request.session['email'])
        wd = wishlist.objects.get(id=id)
        wd.delete()
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=logindata))
        return redirect('/wishlist', {'wish': wd}, locals())