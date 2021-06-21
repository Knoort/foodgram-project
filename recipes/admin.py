from django.contrib import admin
from foodgram.autoregister import autoregister
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from .models import Recipe, Favorites


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'image', 'author', 'pub_date', 'cooking_time', 'fav_cnt'
    )
    search_fields = ('name', )
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientsInline, )
    empty_value_display = '-пусто-'

    def fav_cnt(self, obj):
        return obj.admirers.all().count()

    fav_cnt.short_description = 'Избран'


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe_link', 'user_link')

    def recipe_link(self, obj):
        url = (
            reverse('admin:recipes_recipe_changelist')
            + '?' + urlencode({"id": f"{obj.recipe.id}"})
        )
        return format_html("<a href='{}'>{}</a>", url, obj.recipe.id)

    def user_link(self, obj):
        url = (
            reverse('admin:auth_user_changelist')
            + '?' + urlencode({"id": f"{obj.user.id}"})
        )
        return format_html("<a href='{}'>{}</a>", url, obj.user.username)

    recipe_link.short_description = 'Рецепт'
    user_link.short_description = 'Выбравший'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites, FavoritesAdmin)
autoregister('recipes', )
