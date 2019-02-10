from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
#
from just_shop.settings import MY_WEBSITE_NAME, CATEGORY_PATH_SEPARATOR
from .models import Category
from .forms import CategoryForm
from .utils import get_full_path


# LIST
@login_required
@staff_member_required
def category_list(request):
    categories = Category.objects.all().order_by('full_path', )
    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'Categories',
        'cart': request.user.cart,
        'categories': categories,
    }
    return render(request, 'shop/category/category-list.html', context)


# VALIDATE PATH
def is_new_full_path_valid(request, category_id=0):
    """
    Ensure that the new name does not contain CATEGORY_PATH_SEPARATOR and does not collide with another category.
    """
    post_data = request.POST
    if CATEGORY_PATH_SEPARATOR in post_data['name']:
        messages.error(request, f'Category name cannot contain {CATEGORY_PATH_SEPARATOR}', extra_tags='danger')
        return False
    new_parent_path = (Category.objects.get(id=post_data['parent']).full_path + CATEGORY_PATH_SEPARATOR) \
        if post_data['parent'] else ''
    new_path = new_parent_path + post_data['name']
    match = Category.objects.filter(full_path=new_path)
    if match and match[0].id != category_id:
        messages.error(request, f'This category already exists.', extra_tags='danger')
        return False
    return True


# CREATE
@login_required
@staff_member_required
def category_create(request):
    if request.method == "POST":
        is_valid = is_new_full_path_valid(request)
        if is_valid:
            form = CategoryForm(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect('category_list')

    form = CategoryForm()

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'title': 'New Category',
        'cart': request.user.cart,
        'form': form,
    }
    return render(request, 'shop/category/category-new.html', context)


# UPDATE
@login_required
@staff_member_required
def category_update(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        if is_new_full_path_valid(request, category_id):
            post_data = request.POST
            form = CategoryForm(post_data or None, instance=category)
            if form.is_valid():
                form.save()
                set_paths_recursive(category)
                return redirect('shop')

    form = CategoryForm(None, instance=category)
    form.fields['parent'].queryset = Category.objects.exclude(full_path__startswith=category.full_path)

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'cart': request.user.cart,
        'form': form,
        'category': category,
        'full_path': get_full_path(category_id),
    }

    return render(request, 'shop/category/category-edit.html', context)


def set_paths_recursive(category):
    for child in category.sub_categories.all():
        child.full_path = category.full_path + CATEGORY_PATH_SEPARATOR + child.name
        set_paths_recursive(child)


# DELETE
@login_required
@staff_member_required
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        if category.sub_categories.all():
            messages.error(request,
                           f'You cannot delete this category. '
                           f'There are sub-categories. ({category.sub_categories.all().count()})',
                           extra_tags='danger')
        elif category.products.all():
            messages.error(request,
                           f'You cannot delete this category. '
                           f'There are products in it. ({category.products.all().count()})',
                           extra_tags='danger')
        else:
            category.delete()
            return redirect('category_list')

    context = {
        'category': category
    }

    return render(request, 'shop/category/category-delete.html', context)
