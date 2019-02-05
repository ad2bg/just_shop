from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as AuthViewsLogin

from just_shop.settings import MY_WEBSITE_NAME
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    """
    UserModel Register FBV.
    :param request:
    :return: Register page
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # this saves the newly created user
            # username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'{email}, your account has been created! You are now able to log in.')
            return redirect('users-login')
    else:
        form = UserRegisterForm()

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'form': form
    }

    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    """
    Profile FBV.
    :param request:
    :return: Profile page
    """
    if request.method == 'POST':

        u_form = UserUpdateForm(
            request.POST,
            instance=request.user)

        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            print(p_form)
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('users-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'my_website_name': MY_WEBSITE_NAME,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
