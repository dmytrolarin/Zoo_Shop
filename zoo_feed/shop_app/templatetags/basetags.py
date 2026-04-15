from django import template
from shop_app.models import ProductInCart


register = template.Library()

@register.simple_tag(takes_context=True)
def get_amount_prod_in_cart(context):
    """
    Return the total number of products in the current session cart.
    """
    try:
        products = ProductInCart.objects.filter(session_key=context['session_key'])
        if not products:
            return 0
        else:
            quantity_of_all_prod = 0
            for prod in products:
                quantity_of_all_prod += prod.amount
            return quantity_of_all_prod
    except KeyError:
        return 0
