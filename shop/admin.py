from django.contrib import admin
from .models import Category, Product, CartProduct, Cart

LIST_PER_PAGE = 10
SAVE_AS = True
# SAVE_AS_CONTINUE = False
# SAVE_ON_TOP = True


# CATEGORY
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name full_path'.split()
    list_display_links = 'full_path'.split()
    list_editable = 'name '.split()
    list_filter = 'name parent'.split()
    search_fields = 'name '.split()
    fields = 'parent name'.split()
    list_per_page = LIST_PER_PAGE
    save_as = SAVE_AS
    # save_as_continue = SAVE_AS_CONTINUE
    # save_on_top = SAVE_ON_TOP


# PRODUCT
class ProductAdmin(admin.ModelAdmin):
    list_display = 'category name description_shortened price carts_count total_items total_price'.split()
    list_display_links = 'name '.split()
    list_editable = 'price '.split()
    list_filter = 'name price category'.split()
    search_fields = 'name description price'.split()
    fields = 'category name description price image'.split()
    list_per_page = LIST_PER_PAGE
    save_as = SAVE_AS
    # save_as_continue = SAVE_AS_CONTINUE
    # save_on_top = SAVE_ON_TOP


# CART_PRODUCT
class CartProductAdmin(admin.ModelAdmin):
    list_display = 'cart product product_price quantity total_price'.split()
    list_editable = 'quantity '.split()
    list_filter = 'cart product'.split()
    search_fields = 'cart product'.split()
    fields = 'cart product quantity'.split()
    list_per_page = LIST_PER_PAGE
    save_as = SAVE_AS
    # save_as_continue = SAVE_AS_CONTINUE
    # save_on_top = SAVE_ON_TOP


# CART
class CartAdmin(admin.ModelAdmin):
    list_display = 'name email total_products total_items total_price'.split()
    search_fields = 'name email'.split()
    fields = 'name email total_products'.split()
    readonly_fields = 'name email total_products'.split()
    list_per_page = LIST_PER_PAGE
    save_as = SAVE_AS
    # save_as_continue = SAVE_AS_CONTINUE
    # save_on_top = SAVE_ON_TOP


# REGISTER ALL MODELS
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
