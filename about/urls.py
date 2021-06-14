from django.urls import path

from .views import AboutView

app_name = 'about'

urlpatterns = [
    path('author/', AboutView.as_view(page='author'), name='author'),
    path('tech/', AboutView.as_view(page='tech'), name='tech'),
]
