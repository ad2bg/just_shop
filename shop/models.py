from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import escape
from PIL import Image  # pip install pillow


# CATEGORY
class Category(models.Model):
    # parent
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sub_categories')

    # name
    name = models.CharField(max_length=255)

    # full_path
    full_path = models.TextField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_path or ''

    def __setattr__(self, attr_name, val):
        setter_func = 'setter_' + attr_name
        if attr_name in self.__dict__ and callable(getattr(self, setter_func, None)):
            super(Category, self).__setattr__(attr_name, getattr(self, setter_func)(val))
        else:
            super(Category, self).__setattr__(attr_name, val)

    def setter_parent_id(self, val):
        parent_path = Category.objects.get(id=val).full_path if val else ''
        self.set_path(parent_path + settings.CATEGORY_PATH_SEPARATOR + self.name)
        return val

    def setter_name(self, val):
        parent_path = self.parent.full_path if self.parent else ''
        self.set_path(parent_path + settings.CATEGORY_PATH_SEPARATOR + val)
        return escape(val)

    def set_path(self, path):
        path = path.strip(settings.CATEGORY_PATH_SEPARATOR)
        if self.full_path == path:
            return
        self.full_path = path
        self.save()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('full_path',)


# PRODUCT
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(
        default=settings.PRODUCT_IMAGES_DEFAULT_FILENAME,
        upload_to=settings.PRODUCT_IMAGES_FOLDER,
        blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    carts = models.ManyToManyField('Cart', through='CartProduct', related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def description_shortened(self):
        return self.description[:50]

    @property
    def carts_count(self):
        return self.carts.count()

    @property
    def total_items(self):
        t = 0
        for cp in self.product_carts.all():
            t += cp.quantity
        return t

    @property
    def total_price(self):
        return self.price * self.total_items

    @property
    def image_file(self):
        return self.image.name or ''

    def save(self, **kwargs):
        """
        Auto-resize images. Also fall back to the default image when necessary.
        :return: void
        """

        # fall back to the default value if the user clears the image using the form
        self.image.name = self.image.name or settings.PRODUCT_IMAGES_DEFAULT_FILENAME
        super().save()
        # resize image
        img = Image.open(self.image.path)
        max_size = settings.PRODUCT_IMAGES_MAX_SIZE
        if img.height > max_size or img.width > max_size:
            output_size = (max_size, max_size)
            img.thumbnail(output_size)
            img.save(self.image.path)


# CART_PRODUCT
class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name="cart_products")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_carts")
    quantity = models.DecimalField(decimal_places=0, max_digits=10)

    @property
    def product_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        user_name = self.cart.user.name
        return f"{user_name}'s cart: " \
            f"{self.product.name} : {self.quantity} x ${self.product_price} = ${self.total_price}"


# CART
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', null=True)

    def __str__(self):
        return f"{self.name}'s cart"

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email

    @property
    def total_products(self):
        return len(self.cart_products.all())

    @property
    def total_items(self):
        q = 0
        for cp in self.cart_products.all():
            q += cp.quantity
        return q

    @property
    def total_price(self):
        p = 0
        for cp in self.cart_products.all():
            p += cp.quantity * cp.product.price
        return p


# @receiver(post_save, sender=UserModel)
def create_cart(sender, instance, created=False, **kwargs):
    print('create_cart')
    if created:
        Cart.objects.create(user=instance)


subscribe_to_post_user_create = receiver(post_save, sender=settings.AUTH_USER_MODEL)
create_cart = subscribe_to_post_user_create(create_cart)


# @receiver(post_save, sender=UserModel)
def save_cart(sender, instance, **kwargs):
    print('save_cart')
    instance.cart.save()


subscribe_to_post_user_save = receiver(post_save, sender=settings.AUTH_USER_MODEL)
save_cart = subscribe_to_post_user_save(save_cart)
