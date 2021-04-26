from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter

from recipes.models import Ingredient
from .serializers import IngredientSerializer

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