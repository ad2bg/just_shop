from decimal import Decimal

from .models import Category, CartProduct


def get_full_path(cat_id):
    """
    Returns a list of tuples (category_id, category_name) of the full path;
     used for the breadcrumbs
    :param cat_id:
    :return: List of tuples (category_id, category_name)
    """
    full_path = []
    category = Category.objects.get(id=cat_id)
    while True:
        full_path.append((category.id, category.name))
        parent = category.parent
        if parent is None:
            break
        category = parent
    full_path.reverse()
    return full_path


def add_product_to_cart(cart, product, quantity):
    quantity = Decimal(quantity)
    cp = cart.cart_products.filter(product_id=product.id)
    if cp:
        cp = cp[0]
        cp.quantity += quantity
    else:
        cp = CartProduct(cart=cart, product=product, quantity=quantity)
    cp.save()
