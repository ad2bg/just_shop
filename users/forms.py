from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModel, Profile


class UserRegisterForm(UserCreationForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ['name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ['name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['image']

