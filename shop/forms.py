from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'category name price description'.split()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = 'parent name description'.split()
