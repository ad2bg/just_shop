from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#
from just_shop.settings import MY_WEBSITE_NAME
from .models import Category, Product
from .utils import get_full_path


# SHOP
# @login_required
def shop(request, category_id=None):
    category = None
    full_path = []
    products = []

    if category_id:
        category = Category.objects.get(id=category_id)
        full_path = get_full_path(category_id)
        categories = Category.objects.filter(parent_id=category_id)
        products = Product.objects.filter(category_id=category_id)
    else:
        categories = Category.objects.filter(parent__isnull=True)

    categories = categories.order_by('name')

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'Shop',
        'cart': request.user.cart if request.user.is_authenticated else None,
        'category_name': category.name if category_id else 'Shop',
        'category_id': category_id,
        'full_path': full_path,
        'categories': categories,
        'products': products,
    }

    return render(request, 'shop/shop.html', context)


# CART
@login_required
def cart(request):
    the_cart = request.user.cart
    post_data = request.POST

    print('cart:')
    print(list(the_cart.cart_products.all()))
    print('POST:')
    print(post_data)

    if post_data:
        submit = post_data['submit']
        cp_id = post_data['cp_id']
        if submit == 'remove':
            the_cart.cart_products.get(id=cp_id).delete()
        if submit == 'quantity':
            cp = the_cart.cart_products.get(id=cp_id)
            cp.quantity = post_data.get('quantity', 0)
            cp.save()

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'Cart',
        'cart': the_cart,
    }
    return render(request, 'shop/cart.html', context)


# CART EMPTY
@login_required
def cart_empty(request):
    the_cart = request.user.cart
    the_cart.products.clear()
    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'Cart',
        'cart': the_cart,
    }
    return render(request, 'shop/cart.html', context)


# CART CHECKOUT
@login_required
def cart_checkout(request):
    the_cart = request.user.cart
    purchased = list(the_cart.cart_products.all())
    totals = {
        'products_count': the_cart.total_products,
        'items_count': the_cart.total_items,
        'total_price': the_cart.total_price,
    }
    the_cart.products.clear()

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'Done!',
        'cart': the_cart,
        'purchased': purchased,
        'totals': totals,
        'message': "Your order is now complete.\n"
                   "We deliver to your front door 24/7.\n"
                   "Thank you for shopping with us!\n"
                   "Enjoy your day!".split('\n')
    }
    return render(request, 'shop/checkout.html', context)
