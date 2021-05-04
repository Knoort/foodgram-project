from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from recipes.models import Ingredient, Favorites, Subscriptions
from .serializers import (
    IngredientSerializer,
    FavoritesSerializer,
    SubscriptionsSerializer
)

# Create your views here.
class IngredientViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):

    queryset = Ingredient.objects.all()
    #permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    #pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ('^name', )
    # filterset_fields = ['^name']


class CreateDestroyViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    pass


class FavoritesViewSet(CreateDestroyViewset):

    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesSerializer
    #pagination_class = CustomPagination
    lookup_field = 'recipe'
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]


class SubscriptionsVievSet(CreateDestroyViewset):
    queryset = Subscriptions.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionsSerializer
    lookup_field = 'author'