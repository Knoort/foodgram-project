from django.contrib import admin
from foodgram.autoregister import autoregister

from .models import Recipe, RecipeTag, RecipeIngredients, Ingredient
# Register your models here.


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsInline, )
    list_display = ('id', 'name', 'image', 'author', 'tags', 'pub_date')
    search_fields = ('name', )
    list_filter = ('author', 'name', 'tags')


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


autoregister('recipes', )
