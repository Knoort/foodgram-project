from django.urls import include, path

from foodgram.settings import MEDIA_ROOT
from .views import (
    new_edit_recipe,
    recipe_view_redirect,
    recipe_view_slug,
    recipes_set,
    subscriptions,
    INDEX,
    AUTHOR_PROF,
    FAVORITES,
    SUBSCRIPTIONS
)

app_name = 'recipes'

favorites_urls = [
    path('', recipes_set, name=FAVORITES, kwargs={'page_choice': FAVORITES})
]
subscriptions_urls = [
    path('', subscriptions, name=SUBSCRIPTIONS)
]


urlpatterns = [
    path('', recipes_set, name=INDEX, kwargs={'page_choice': INDEX}),
    path('new/', new_edit_recipe, name='new_recipe'),
    path('favorites/', include(favorites_urls)),
    path('subscriptions/', include(subscriptions_urls)),
    path('<int:recipe_id>/<str:slug>/edit/', new_edit_recipe, name='edit_recipe'),
    path('<int:recipe_id>/<str:slug>/', recipe_view_slug, name='recipe_view_slug'),
    path('<int:recipe_id>/', recipe_view_redirect, name='recipe_view_redirect'),
    path(
        '<str:author_username>/',
        recipes_set,
        name=AUTHOR_PROF,
        kwargs={'page_choice': AUTHOR_PROF}
    ),
]

