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
    # author = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     # queryset=User.objects.all()
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscriptions
        fields = ('author', 'user')

    def validate_author(self, author):
        # print('validate author: ', author)
        return author

    def validate(self, attrs):
        if attrs.get('author', None) == attrs.get('user', None):
            raise serializers.ValidationError(
                'You cannot follow Yourself!'
            )
        return attrs
        

class PurchasesSerializer(serializers.ModelSerializer):
    # recipe = serializers.IntegerField()
    # recipe = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Purchases
        fields = ('recipe', 'user', )
    
    def validate_recipe(self, recipe):
        print('validate recipe: ', recipe)
        return recipe
    
    def validate_user(self, user):
        print('validate user: ', user)
        return user
