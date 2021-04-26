from django.urls import path

from foodgram.settings import MEDIA_ROOT
from .views import new_recipe, recipe_view_redirect, recipe_view_slug

# media_urls = 

urlpatterns = [
    path('new/', new_recipe, name='new_recipe'),
    path('<int:recipe_id>/', recipe_view_redirect, name='recipe_view_redirect'),
    path('<int:recipe_id>/<str:slug>/', recipe_view_slug, name='recipe_view_slug'),
]