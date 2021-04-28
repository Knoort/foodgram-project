from django.urls import path

from foodgram.settings import MEDIA_ROOT
from .views import (
    new_recipe,
    edit_recipe,
    recipe_view_redirect,
    recipe_view_slug,
    index,
)

# media_urls = 

urlpatterns = [
    path('', index, name='index'),
    path('new/', new_recipe, name='new_recipe'),
    path('<int:recipe_id>/<str:slug>/edit/', edit_recipe, name='edit_recipe'),
    path('<int:recipe_id>/<str:slug>/', recipe_view_slug, name='recipe_view_slug'),
    path('<int:recipe_id>/', recipe_view_redirect, name='recipe_view_redirect'),
    path('<str:author_username>/', index, name='author_profile')
]