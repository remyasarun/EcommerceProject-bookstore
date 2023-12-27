from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('register', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('category<slug:val>', views.Category.as_view(), name='category'),
    path('productdetails<int:pk>', views.Productdetails.as_view(), name='productdetails'),
    path('search', views.search, name='search'),

    path('profile', views.Profile.as_view(), name='profile'),
    path('address', views.address, name='address'),
    path('updateaddress<int:pk>', views.updateaddress.as_view(), name='updateaddress'),

    path('addtocart', views.addtocart, name='addtocart'),
    path('cart', views.Showcart, name='showcart'),
    path('removecart/<int:id>', views.remove_cart, name='removecart'),
    # path('buynow/<int:id>', views.Buynow.as_view(), name='buynow'),

    path('checkoutpage', views.checkout.as_view(), name='checkoutpage'),
    path('orders', views.orders, name='orders'),
    path('paymentdone', views.paymentdone, name='paymentdone'),

    path('COD', views.COD, name='COD'),

    path('base', views.Base, name='base'),
    path('footer', views.Footer, name='footer'),

    path('wishlist', views.Wishlist, name='wishlist'),
    path('showwishlist', views.Show_wishlist, name='showwishlist'),
    path('removewishlist/<int:id>', views.remove_wishlist, name='removewishlist'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'BOOKMART'
admin.site.site_title = 'BOOKMART'
admin.site.site_home_title = 'BOOKMART'