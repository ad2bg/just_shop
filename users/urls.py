from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from just_shop.settings import MY_WEBSITE_NAME

extra_context = {
    'my_website_name': MY_WEBSITE_NAME,
}

urlpatterns = [

    path('register/', views.register, name='users-register'),
    path('profile-info/', views.profile_info, name='users-profile'),
    path('profile-photo/', views.profile_photo, name='users-profile_photo'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context=extra_context),
         name='users-login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', extra_context=extra_context),
         name='users-logout'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', extra_context=extra_context),
         name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html', extra_context=extra_context), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html', extra_context=extra_context), name='password_reset_confirm'),

    path(r'password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html', extra_context=extra_context),
         name='password_reset_complete'),
]
