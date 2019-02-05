from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # substituting the default Django User model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image  # pip install pillow

DEFAULT_PROFILE_IMAGE_FILENAME = 'users/default.jpg'
DEFAULT_PROFILE_IMAGES_FOLDER = 'users/photos'
# DEFAULT_PRODUCT_IMAGE_FILENAME = 'products/default.png'
# DEFAULT_PRODUCT_IMAGES_FOLDER = 'products/photos'


class UserModelManager(BaseUserManager):
    """Allow Django to work with the custom 'UserModel' user model."""

    def create_user(self, email, name, password):
        """Creates a new user profile object."""

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)  # this hashes the password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with giver details."""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Substitute the default Django 'User' model.
    Use the email address for authentication instead of a username.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a user's full name."""
        return f'{self.name} ({self.email})'

    def get_short_name(self):
        """Used to get a user's short name."""
        return self.name

    # @property
    # def total_tickets(self):
    #     return len(self.tickets.all())

    def __str__(self):
        """Django uses this when it needs to convert the object to a string."""
        return self.email

    class Meta:
        verbose_name = 'User'
        ordering = ('name',)


class Profile(models.Model):
    """
    One-To-One relation to the UserModel.
    """

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile', null=True)
    image = models.ImageField(
        default=DEFAULT_PROFILE_IMAGE_FILENAME,
        upload_to=DEFAULT_PROFILE_IMAGES_FOLDER,
        blank=True, null=True)

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email

    @property
    def image_file(self):
        return self.image.name or ''

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def is_staff(self):
        return self.user.is_staff

    @property
    def is_superuser(self):
        return self.user.is_superuser

    # @property
    # def total_tickets(self):
    #     return len(self.user.tickets.all())

    def __str__(self):
        return f'{self.user.name}\'s Profile'

    def save(self, **kwargs):
        """
        Auto-resize images. Also fall back to the default image when necessary.
        :return: void
        """

        # fall back to the default value if the user clears the image using the form
        self.image.name = self.image.name or DEFAULT_PROFILE_IMAGE_FILENAME

        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# @receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created=False, **kwargs):
    print('create_profile')
    if created:
        Profile.objects.create(user=instance)


subscribe_to_post_user_create = receiver(post_save, sender=settings.AUTH_USER_MODEL)
create_profile = subscribe_to_post_user_create(create_profile)


# @receiver(post_save, sender=UserModel)
def save_profile(sender, instance, **kwargs):
    print('save_profile')
    instance.profile.save()


subscribe_to_post_user_save = receiver(post_save, sender=settings.AUTH_USER_MODEL)
save_profile = subscribe_to_post_user_save(save_profile)
