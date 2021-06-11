from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Favorites,
    Recipe,
    Subscriptions,
    Purchases
)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'units')


class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorites
        fields = ('recipe', 'user')


class SubscriptionsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscriptions
        fields = ('author', 'user')

    def validate(self, attrs):
        author = attrs.get('author', None)
        user = attrs.get('user', None)
        if author and author == user:
            raise serializers.ValidationError(
                'You cannot follow Yourself!'
            )
        return attrs
        

class PurchasesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Purchases
        fields = ('recipe', 'user', )
