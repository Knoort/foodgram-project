from django.urls import include, path
from . import views

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    # её полный адрес будет auth/signup/, но префикс auth/ обрабатывается в головном urls.py
    path("signup/", views.SignUp.as_view(), name="signup"),
    #  если нужного шаблона для /auth не нашлось в файле users.urls — 
    #  ищем совпадения в файле django.contrib.auth.urls
    path("", include("django.contrib.auth.urls")),
] 