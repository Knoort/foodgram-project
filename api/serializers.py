from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Favorites,
    Recipe,
    Subscriptions
)

User = get_user_model()

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'units')


class FavoritesSerializer(serializers.ModelSerializer):
    # recipe = serializers.PrimaryKeyRelatedField(
    #     queryset=Recipe.objects.all(),
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Favorites
        fields = ('recipe', 'user')


class SubscriptionsSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     # queryset=User.objects.all()
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Subscriptions
        fields = ('author', 'user')