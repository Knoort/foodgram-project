from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet


router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('v1/', include(router.urls)),
]