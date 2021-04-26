from django.contrib import admin
from foodgram.autoregister import autoregister

from .models import Recipe, RecipeTag, RecipeIngredients, Ingredient
# Register your models here.

class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsInline, )

autoregister('recipes', )