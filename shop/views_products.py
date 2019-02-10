from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET
#
from just_shop.settings import MEDIA_URL, MY_WEBSITE_NAME, PRODUCT_IMAGES_DEFAULT_FILENAME
from .forms import ProductForm
from .models import Product
from .utils import add_product_to_cart

# Note: We can comment out @login_required or @staff_member_required  as per the desired business logic;
# For now, only admins can add/edit/delete products, so we go with the staff member requirement.


# LIST
@require_GET
def product_list(request):
    products = Product.objects.all().order_by('name', )
    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'Products',
        'cart': request.user.cart if request.user.is_authenticated else None,
        'products': products,
    }
    return render(request, 'shop/product/product-list.html', context)


# VIEW
@require_http_methods(["GET", "POST"])
def product_view(request, product_id=None):
    qty = None
    if request.method == 'POST':
        post_data = request.POST
        product_id = post_data['product_id']
        qty = post_data['quantity']

    product = Product.objects.filter(id=product_id)[0]

    if request.method == 'POST' and request.user.is_authenticated:
        add_product_to_cart(request.user.cart, product,qty)
        messages.success(request, f'Added to cart: {qty} x {product.name}')
        return redirect('shop', product.category.id)

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': product.name,
        'cart': request.user.cart if request.user.is_authenticated else None,
        'product': product,
        'default_product_image_filename': PRODUCT_IMAGES_DEFAULT_FILENAME,
    }
    return render(request, 'shop/product/product-view.html', context)


# CREATE
@login_required
@staff_member_required
@require_http_methods(["GET", "POST"])
def product_create(request):

    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = Product(
            category=form.cleaned_data.get('category'),
            name=form.cleaned_data.get('name'),
            description=form.cleaned_data.get('description'),
            price=form.cleaned_data.get('price'),
        )
        if request.FILES:
            product.image = request.FILES['image']
        product.save()
        messages.success(request, f"Created product: {form.cleaned_data.get('name')}")
        return redirect('product_list')

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'New Product',
        'cart': request.user.cart,
        'form': form,
        'default_product_image_filename': MEDIA_URL + PRODUCT_IMAGES_DEFAULT_FILENAME,
    }

    return render(request, 'shop/product/product-new.html', context)


# UPDATE
@login_required
@staff_member_required
@require_http_methods(["GET", "POST"])
def product_update(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        if request.FILES:
            product.image = request.FILES['image']
            product.save()
        messages.success(request, f"Updated product: {product.name}")
        return redirect('product_list')

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'cart': request.user.cart,
        'form': form,
        'product': product,
        'default_product_image_filename': PRODUCT_IMAGES_DEFAULT_FILENAME,
    }

    return render(request, 'shop/product/product-edit.html', context)


# DELETE
@login_required
@staff_member_required
@require_http_methods(["GET", "POST"])
def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Deleted product: {name}")
        return redirect('product_list')

    context = {
        'product': product
    }

    return render(request, 'shop/product/product-delete.html', context)
