from django.shortcuts import render, redirect
from shop_app.models import*
from .utils import *
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.sessions.models import Session

def show_home_page(request):
    """
    Render the home page and handle general form submissions.
    """
    context={
        'title':'Zoo Feed - food for cats and dogs',
        'session_key': request.session.session_key
        }
    if request.method == 'POST':
        context['is_sending_success'] = handle_forms(request.POST)
    return render(request, 'shop_app/home.html', context=context)

def show_assortment_page(request):
    """
    Render the assortment page for the selected product type.
    """
    type_of_products = request.GET.get('type_of_products')
    # Try to get the product type from the URL parameter.
    try:
        type_of_products_id = TypeOfProduct.objects.get(url_name = type_of_products)
    except TypeOfProduct.DoesNotExist:
        return redirect('home')
    # Get brands for the selected product type.
    all_brands = Brand.objects.filter(type_of_products=type_of_products_id)
    context={'title':'Assortment',
            'eco_brands':all_brands.filter(segment='eco'),
            'premium_brands':all_brands.filter(segment='premium'),
            'super_premium_brands':all_brands.filter(segment='super-premium'),
            'type_of_products': type_of_products,
            'session_key': request.session.session_key
            }
    if request.method == 'POST':
        context['is_sending_success'] = handle_forms(request.POST)  
    return render(request, 'shop_app/assortment.html',  context=context)

def show_products_page(request):
    """
    Render the products page with filtering, pricing, and session setup.
    """
    type_of_products = request.GET.get('type_of_products')
    brand = request.GET.get('brand')
    absolute_uri = request.build_absolute_uri()
    # Try to get the product type and brand from the URL parameters.
    try:
        type_of_products_id = TypeOfProduct.objects.get(url_name = type_of_products)
        brand_id = Brand.objects.get(name = brand)
    except (TypeOfProduct.DoesNotExist, Brand.DoesNotExist):
        return redirect('home')
    # Filter products by brand and type.
    products = Product.objects.filter(brand_id=brand_id, type_of_product_id=type_of_products_id)
    # Get the absolute price range used for product filtering.
    absolute_min_price, absolute_max_price = get_absolute_price_range(products)
    
    filters_ids = []
    # Apply filters selected by the user.
    if 'filters' in absolute_uri:
        filters_ids = get_filters_ids_from_uri(absolute_uri)
        if filters_ids:
            products = Product.get_products_by_filters(products, filters_ids)
        else:
            return redirect('home')
    # Get the price range selected by the user.
    min_price, max_price  = get_price_range_from_uri(absolute_uri)
    # Validate the selected price range.
    # If it is invalid, fall back to the absolute available range.
    if min_price == None and max_price == None: 
        min_price, max_price = absolute_min_price, absolute_max_price
    elif absolute_min_price  > min_price or max_price > absolute_max_price or absolute_min_price  > max_price or min_price > absolute_max_price:
        min_price, max_price = absolute_min_price, absolute_max_price
        
    product_packings = []
    list_stocks = []
    products_to_delete = []
    # Build lists of packings and discount flags.
    for product in products:
        packings_for_this_product = Packing.objects.filter(product_id=product.pk).order_by('weight')
        packings_for_this_product = packings_for_this_product.filter(current_price__gte=min_price)
        packings_for_this_product = packings_for_this_product.filter(current_price__lte=max_price)
        if packings_for_this_product:
            product_packings += [packings_for_this_product]
            for packing in packings_for_this_product:
                if packing.old_price:
                    list_stocks.append('stock')
                    break
            else:
                list_stocks.append(False)
        else:
            products_to_delete.append(product)
    products = list(products)
    for product in products_to_delete:
        products.remove(product)   
    # Get filter groups and filter items available for this product type.
    filter_groups = FilterGroup.objects.filter(type_of_products = type_of_products_id)
    filter_items = []
    for fg in filter_groups:
        filter_items += [FilterItem.objects.filter(filter_group_id = fg.pk)]
    
    type_of_products_object = TypeOfProduct.objects.get(url_name=type_of_products)
    context={'title':f'{type_of_products_object} - {brand} ', 
             'type_of_products':type_of_products_object,
             'products': products, 
             'product_packings':product_packings,
             'filter_groups':filter_groups,
             'filter_items':filter_items,
             'list_stocks':list_stocks,
             'current_url':absolute_uri,
             'filters_applied': True if 'filters' in absolute_uri else False,
             'filters_ids':filters_ids,
             'min_price':min_price,
             'max_price':max_price,
             'absolute_min_price':absolute_min_price,
             'absolute_max_price':absolute_max_price,
             'session_key': request.session.session_key
             }
    
    if request.method == 'POST':
        context['is_sending_success'] = handle_forms(request.POST)
    # Create a session key if it does not exist.
    session_key = request.session.session_key
    if not session_key:
        # Remove expired sessions and related cart items.
        call_command('clearsessions')
        for pic in ProductInCart.objects.all():
            try: 
                Session.objects.get(session_key=pic.session_key)
            except:
                pic.delete()
        # Create a new session key.
        request.session.cycle_key()
    context['session_key'] = session_key
    
    return render(request, 'shop_app/products.html', context=context)

def show_product_view(request, vendor_code):
    """
    Render the detailed page for a single product.
    """
    product = Product.objects.get(vendor_code = vendor_code)
    product_packings = Packing.objects.filter(product_id=product.pk).order_by('weight')
    brand = Brand.objects.get(pk = product.brand_id)
    segment = brand.get_segment_display()
    # Check whether the product has an active promotion.
    is_promotion = False
    for packing in product_packings:
        if packing.old_price:
            is_promotion = True
            break

    context = {
        'title':'Product overview', 
        'product':product,
        'product_packings': product_packings,
        'brand': brand,
        'segment': segment,
        'session_key': request.session.session_key,
        'is_promotion':is_promotion
    }
    if request.method == 'POST':
        context['is_sending_success'] = handle_forms(request.POST)
    return render(request, 'shop_app/product_view.html', context=context)

def show_cart(request):
    """
    Render the cart page and handle order-related form submissions.
    """
    context = {
        'title':'Cart',
        'session_key': request.session.session_key
    }

    if request.method == 'POST':
        # Process the order form.
        if request.POST.get('form_name') == 'order':
            context = context | handle_order(request.POST, context['session_key'])
        # Process the remaining forms.
        else:
            context['is_sending_success'] = handle_forms(request.POST)

    context['products_in_cart'] = ProductInCart.objects.filter(session_key=request.session.session_key)

    if context['products_in_cart']:
        context['current_full_price'], context['old_full_price'] = get_full_order_prices(context['products_in_cart'])

    return render(request, 'shop_app/cart.html', context=context)

def add_product_to_cart(request):
    """
    Add a selected product packing to the current session cart.
    """
    session_key = request.session.session_key
    data = request.POST
    product_pk = data.get('product_pk')
    product_amount = data.get('product_amount')
    packing_pk = data.get('packing_pk')
    # Try to find the product in the cart.
    product_in_cart = ProductInCart.objects.filter(session_key=session_key, product_id=product_pk, packing_id=packing_pk)
    # If the product is not in the cart yet, add it.
    if not product_in_cart:
        # Verify that the product and packing exist and belong together.
        try:
            Product.objects.get(pk=product_pk)
            packing = Packing.objects.get(pk=packing_pk)
            
            if packing.product.pk == int(product_pk):
                ProductInCart.objects.create(session_key=session_key,product_id=product_pk,amount=product_amount, packing_id=packing_pk)      
        except:
            None
    # Otherwise, just increase the product quantity in the cart.
    else:
        product_in_cart = product_in_cart[0]
        product_in_cart.amount += int(product_amount)
        product_in_cart.save()
    return HttpResponse(None)

def del_prod_from_cart(request):
    """
    Remove a product from the current session cart.
    """
    session_key = request.session.session_key
    data = request.POST
    prod_in_cart_pk = data.get('prod_in_cart_pk')
    prod_in_cart_lst = ProductInCart.objects.filter(pk=prod_in_cart_pk, session_key=session_key)
    if prod_in_cart_lst:
        prod_in_cart_lst[0].delete()
    return HttpResponse(None)

def udpate_amount_prod_in_cart(request):
    """
    Update the quantity of a product already stored in the cart.
    """
    session_key = request.session.session_key
    data = request.POST
    prod_in_cart_pk = data.get('prod_in_cart_pk')
    updated_amount = data.get('updated_amount')
    prod_in_cart_lst = ProductInCart.objects.filter(pk=prod_in_cart_pk, session_key=session_key)
    if prod_in_cart_lst:
        prod_in_cart_lst[0].amount = updated_amount
        prod_in_cart_lst[0].save()
    return HttpResponse(None)

def show_terms_of_use(request):
    """
    Render the terms of use page.
    """
    return render(request, 'shop_app/terms_of_use.html', context={'session_key': request.session.session_key,})

def show_contract_offer(request):
    """
    Render the contract offer page.
    """
    return render(request, 'shop_app/contract_offer.html', context={'session_key': request.session.session_key,})
