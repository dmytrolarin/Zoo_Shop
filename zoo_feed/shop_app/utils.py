from django.shortcuts import redirect
from django.core.mail import send_mail
from zoo_feed import settings
from .models import *

 
def get_filters_ids_from_uri(path):
    """
    Return a list of filter IDs from the URL selected by the user.
    """
    all_parameters = path.split('?')[-1]
    result= None
    for parameter in all_parameters.split('&'):
        if parameter.startswith('filters='):
            ids = parameter.split('=')[-1]
            try:
                if ids:
                    ids = ids.split(',')
                    ids = list(map(int, ids))
                    result =  ids
            except:
                pass  
    return result
 
def get_price_range_from_uri(path):
    """
    Return the user-selected price range from the URL as [a, b].
    """
    all_parameters = path.split('?')[-1]
    for parameter in all_parameters.split('&'):
        if parameter.startswith('price_range='):
            try: 
                price_range =  list(map(int, parameter.split('=')[-1].split(',')))
                break  
            except:
                price_range = [None, None]
    else:
        price_range = [None, None]
    if price_range[0] and price_range[1]:
        if price_range[0] > price_range[1]:
            price_range = [None, None]
    return price_range  

def get_absolute_price_range(products):
    """
    Return the price range for a collection of products as [a, b].
    """
    min_price = None
    max_price = None
    for prod in products:
        packings_for_this_product = Packing.objects.filter(product_id=prod.pk).order_by('weight')
        for packing in packings_for_this_product:
            if max_price == None and min_price == None:
                max_price = packing.current_price
                min_price = packing.current_price
            else:
                if min_price > packing.current_price:
                    min_price = packing.current_price
                elif max_price < packing.current_price:
                    max_price = packing.current_price

    return [min_price, max_price]

def handle_forms(post_data):
    """
    Handle consultation and review forms and return the mail result.
    """
    if post_data.get('form_name')  == 'consultation':
        subject = 'Consultation request'
        message =   f"""Client: {post_data.get('client_name')};
            \rPhone number: {post_data.get('phone_number')}; 
            \rAnimal breed: {post_data.get('animal')}; 
            \rAnimal age: {post_data.get('age_of_animal')};"""
    elif post_data.get('form_name') == 'review':
        subject = 'Review'
        message =   f"""Client: {post_data.get('client_name')};
            \rClient email: {post_data.get('client_email')}; 
            \rClient impression: {post_data.get('impression')}; """ 
    try:
        mail = send_mail(subject,message,settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    except:
        mail = False
    return mail

def get_full_order_prices(prod_in_cart_list):
    """
    Return (current_price, old_price) for the full order.
    """
    current_full_price = 0
    old_full_price = 0
    for prod_in_cart in prod_in_cart_list:
        product_amount = prod_in_cart.amount
        current_full_price += prod_in_cart.packing.current_price*product_amount
        if prod_in_cart.packing.old_price:
            old_full_price += prod_in_cart.packing.old_price*product_amount
        else:
            old_full_price += prod_in_cart.packing.current_price*product_amount
    if current_full_price == old_full_price:
        old_full_price = None
    return (current_full_price, old_full_price)

def handle_order(post_data, session_key):
    """
    Handle the customer order and send emails to the client and admin.

    Returns different context values depending on the outcome:
    {'cart_empty_error': True} - the cart was empty

    {
    'order_processed': True,
    'phone_number': post_data.get('phone_number')
    } - successful submission

    {'send_error': True} - sending error
    """
    products_in_cart = ProductInCart.objects.filter(session_key=session_key)
    # If the cart is empty.
    if len(products_in_cart) == 0:
        context = {'cart_empty_error':True}
    else:
        # Build the order summary string.
        order_string = ''
        for prod_in_cart in products_in_cart:
            order_string += f'{prod_in_cart.product.name}, {prod_in_cart.packing.weight} kg, {prod_in_cart.amount} pcs.\n'
        # Get the order price.
        order_price = get_full_order_prices(products_in_cart)[0]
        # Build the delivery method string.
        if post_data.get('order-receiving') == 'pickup':
            order_receiving_string = 'Pickup'
        elif post_data.get('order-receiving') == 'ukrposhta':
            order_receiving_string = f"Ukr Post.\nPostal code: {post_data.get('ukrposhta_index')}"
        elif post_data.get('order-receiving') == 'nova_poshta':
            order_receiving_string = "Nova Post."
        elif post_data.get('order-receiving') == 'justin':
            order_receiving_string = "Justin."
        if post_data.get('order-receiving') == 'justin' or post_data.get('order-receiving') == 'nova_poshta':
            order_receiving_string += f"\nCity: {post_data.get('city')}\nDepartment number: {post_data.get('department_number')}"    
        # Build the email for the client.
        subject_client = 'Thank you for your order!'
        message_client =   f"""Thank you for your order at the Zoo Feed pet food store!
            \rYour order is being processed by a manager. Within 15-30 minutes they will contact you at {post_data.get('phone_number')}.
            \rYour order:\n{order_string}\nOrder price: {order_price} USD
            \rDelivery method: {order_receiving_string}"""
        # Build the client comment string.
        client_comment = post_data.get('comment')
        if client_comment:
            client_comment = f'Order comment:\n{client_comment}'
        else:
            client_comment = ''
        # Build the email for the admin.
        subject_admin = 'New order'
        message_admin =   f"""New order from client {post_data.get('name')} {post_data.get('surname')} {post_data.get('patronymic')}.\nClient phone: {post_data.get('phone_number')}.\nClient email: {post_data.get('email')}.
            \rOrder:\n{order_string}\nOrder price: {order_price} USD
            \rDelivery method: {order_receiving_string}
            \r{client_comment}"""
        # Send the emails.
        try:
            mail_client = send_mail(subject_client,message_client,settings.EMAIL_HOST_USER,[post_data.get('email')])
            mail_admin = send_mail(subject_admin,message_admin,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER])
        except:
            mail_client = False
            mail_admin = False
        # If sending was successful.
        if mail_client or mail_admin:
            context = {
                'order_processed':True,
                'phone_number':post_data.get('phone_number')
                }
            products_in_cart.delete()
        else:
            context = {'send_error':True}
        
    return context
