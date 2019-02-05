from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse

from just_shop.settings import MY_WEBSITE_NAME


# @login_required
def home(request):
    context = {'my_website_name': MY_WEBSITE_NAME, 'title': 'Products'}
    return render(request, 'main/shop.html', context)


@login_required
def cart(request):
    context = {'my_website_name': MY_WEBSITE_NAME, 'title': 'Cart'}
    return render(request, 'main/cart.html', context)
