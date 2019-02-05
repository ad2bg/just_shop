from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import UserModel, Profile


LIST_PER_PAGE = 5


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    Includes all the required fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.
    Includes all the fields on the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserModelAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name',
                    'is_active', 'is_staff', 'is_superuser',
                    'created_at', 'updated_at', )
    list_filter = ('name', 'is_active', 'is_staff', 'is_superuser',
                   'created_at', 'updated_at')
    list_editable = ('name', 'is_active', 'is_staff', 'is_superuser',)

    fieldsets = (
        ('Authentication', {'fields': ('email', 'password', 'is_active')}),
        ('Authorization', {'fields': ('is_staff', 'is_superuser')}),
        ('Personal info', {'fields': ('name',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute.
    # UserAdmin overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active')}
         ),
        ('Authorization', {'fields': ('is_staff', 'is_superuser')}),
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('name',)}
         ),
    )
    search_fields = ('name', 'email',)
    ordering = ('email',)
    filter_horizontal = ()
    list_per_page = LIST_PER_PAGE


class ProfileAdmin(admin.ModelAdmin):
    list_display = 'name email image_file is_active is_staff is_superuser'.split()
    list_filter = ('user__name', 'user__is_active', 'user__is_staff', 'user__is_superuser')
    search_fields = ('user__name', 'user__email')
    ordering = ('user__email',)
    list_per_page = LIST_PER_PAGE


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(Profile, ProfileAdmin)
