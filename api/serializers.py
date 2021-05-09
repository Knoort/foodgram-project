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

    def validate_author(self, author):
        print('validate author: ', author)
        return author

class PurchasesSerializer(serializers.ModelSerializer):
    # recipe = serializers.IntegerField()
    # recipe = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Purchases
        fields = ('recipe', 'user', )

    # def get_recipe(self, obj):
    #     recipe = get_object_or_404(Recipe, pk=obj)
    #     print('get recipe:', recipe.id)
    #     return recipe.id

    # def run_validation(self, data):
    #     """
    #     We override the default `run_validation`, because the validation
    #     performed by validators and the `.validate()` method should
    #     be coerced into an error dictionary with a 'non_fields_error' key.
    #     """
    #     print('initial: ', data)
    #     (is_empty_value, data) = self.validate_empty_values(data)
    #     if is_empty_value:
    #         return data

    #     value = self.to_internal_value(data)
    #     print('validated: ', value.get('recipe').id)
    #     try:
    #         self.run_validators(value)
    #         value = self.validate(value)
    #         assert value is not None, '.validate() should return the validated data'
    #     except (ValidationError, DjangoValidationError) as exc:
    #         raise ValidationError(detail=as_serializer_error(exc))

    #     return value
    
    def validate_recipe(self, recipe):
        print('validate recipe: ', recipe)
        return recipe
    
    def validate_user(self, user):
        print('validate user: ', user)
        return user