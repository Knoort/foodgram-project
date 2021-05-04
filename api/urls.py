from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, FavoritesViewSet, SubscriptionsVievSet


router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('favorites', FavoritesViewSet, basename='favorites')
router.register('subscriptions', SubscriptionsVievSet, basename='subscriptions')

urlpatterns = [
    path('v1/', include(router.urls)),
]

print(router.urls)