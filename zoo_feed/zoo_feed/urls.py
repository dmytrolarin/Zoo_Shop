"""zoo_feed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop_app.views import*
from django.conf.urls.static import static
from zoo_feed import settings

urlpatterns = [
    path('5QH8GD4F4aBKkTacuWZc8dL54cSVzAtl/', admin.site.urls),
    path('', show_home_page, name='home'),
    path('assortment/', show_assortment_page, name='assortment'),
    path('products/', show_products_page, name='products'),
    path('product-view/<slug:vendor_code>', show_product_view, name='product_view'),
    path('cart/', show_cart, name='cart' ),
    path('add_product_to_cart/', add_product_to_cart, name='add_product_to_cart' ),
    path('del_prod_from_cart/', del_prod_from_cart, name='del_prod_from_cart'),
    path('udpate_amount_prod_in_cart/', udpate_amount_prod_in_cart, name='udpate_amount_prod_in_cart'),
    path('terms_of_use/', show_terms_of_use, name='terms_of_use'),
    path('contract_offer/', show_contract_offer, name='contract_offer')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
