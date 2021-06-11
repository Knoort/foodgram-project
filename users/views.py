from django.shortcuts import render
from django.views.generic import CreateView
#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("users:login")
    template_name = "reg.html" 
    # namespace = 'users'
