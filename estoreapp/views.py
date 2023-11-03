from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from estoreapp.models import Customer, BOOKDETAILS, Cart


# Create your views here.
def Home(request):
    return render(request, 'home.html')
def Base(request):
    return render(request, 'base.html')
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


class Category(View):
    def get(self, request, val):
        book = BOOKDETAILS.objects.filter(Category=val)
        title = book.filter(Category=val).values('Title')
        return render(request, 'category.html', locals())

class Productdetails(View):
    def get(self, request, pk):
        book = BOOKDETAILS.objects.get(pk=pk)
        return render(request, 'productdetails.html', locals())


def add_to_cart(request):
    email = request.session.get('email')
    print(email)
    product_id = request.GET.get('prod_id')
    print(product_id)
    product = BOOKDETAILS.objects.get(pk=product_id)
    print(product)

    Cart(Email=email, Product=product).save()
    return render(request, 'addtocart.html')

def Showcart(request):
    user = request.Email
    cart = Cart.objects.filter(Email=user)
    return render(request, 'addtocart.html', locals())

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        print(search_query)
        filtered_model = BOOKDETAILS.objects.all().filter(Q(Title__icontains=search_query) | Q(Category__icontains=search_query))
        return render(request, 'search.html', {'search_query': search_query, 'filtered_model': filtered_model})
    else:
        return render(request, 'search_results.html', {})