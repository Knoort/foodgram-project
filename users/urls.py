from django.urls import include, path, reverse_lazy

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView
)

from .views import SignUp

app_name = 'users'

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            success_url=reverse_lazy('users:password_change_done'),
            extra_context={
                'title': 'Изменение пароля',
                'header_title': 'Изменить пароль',
            }
        ),
        name='password_change'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            success_url=reverse_lazy('users:password_reset_done'),
            extra_context={
                'header_title': 'Сброс пароля',
            },
        ),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    #  если нужного шаблона для /auth не нашлось в файле users.urls —
    #  ищем совпадения в файле django.contrib.auth.urls
    path("", include("django.contrib.auth.urls")),
]
