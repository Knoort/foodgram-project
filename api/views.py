from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from recipes.models import Ingredient, Favorites, Subscriptions, Purchases
from .serializers import (
    IngredientSerializer,
    FavoritesSerializer,
    SubscriptionsSerializer,
    PurchasesSerializer
)

# Create your views here.
class IngredientViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ('^name', )
    # filterset_fields = ['^name']


class CreateDestroyViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    def get_object(self, **kwargs):
        """
        Добавлено поле user для поиска объекта
        """
        print('purchases_api')
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            **kwargs
        }
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, **kwargs):
        instance = self.get_object(user=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoritesViewSet(CreateDestroyViewset):
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesSerializer
    lookup_field = 'recipe'


class SubscriptionsVievSet(CreateDestroyViewset):
    queryset = Subscriptions.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionsSerializer
    lookup_field = 'author'


class PurchasesViewSet(
    mixins.ListModelMixin,
    CreateDestroyViewset
    ):
    queryset = Purchases.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = PurchasesSerializer
    lookup_field = 'recipe'