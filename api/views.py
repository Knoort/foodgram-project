from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
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


class IngredientViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ('^name', )


class CreateDestroyViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_object(self, **kwargs):
        """
        Добавлено поле user для поиска объекта
        """
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

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            if not hasattr(self, 'perform_create'):
                raise ImproperlyConfigured(
                    "NotAuthorizedCreateModelMixin requires a definition of"
                    " 'perform_create()' method!"
                )
            serializer.save()
            return
        # Создаем список покупок для неавторизованного юзера.
        # purchases - список идентификаторов рецептов,
        # сохраненный в сессии юзера.
        purchases = self.request.session.get('purchases')
        if not type(purchases) is list:
            purchases = []
        recipe_id = serializer.validated_data['recipe'].id
        if recipe_id not in purchases:
            self.request.session.update({
                'purchases': purchases + [recipe_id]
            })

    def destroy(self, request, **kwargs):
        if request.user.is_authenticated:
            instance = self.get_object(user=request.user)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if not kwargs.get('recipe').isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = int(kwargs.get('recipe'))

        purchases = request.session.get('purchases')
        if not purchases:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if recipe not in purchases:
            return Response(status=status.HTTP_404_NOT_FOUND)
        purchases.remove(recipe)
        request.session['purchases'] = purchases
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
    serializer_class = PurchasesSerializer
    lookup_field = 'recipe'
