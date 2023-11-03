from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('register', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('category<slug:val>', views.Category.as_view(), name='category'),
    path('productdetails<int:pk>', views.Productdetails.as_view(), name='productdetails'),
    path('search', views.search, name='search'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.Showcart, name='showcart'),
    path('base', views.Base, name='base'),
    path('footer', views.Footer, name='footer'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)