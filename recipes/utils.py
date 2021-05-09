from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.utils.text import slugify
# from django.utils import encoding
# from django.template import defaultfilters -> slugify
# import unidecode
from unidecode import unidecode

from .models import Ingredient, RecipeIngredients

def decode_slugify(txt):
    return slugify(unidecode(txt))


def get_ingredients_from_qs(recipe_ings):
    ingredients = {}
    num = 0
    for recipe_ing in recipe_ings:
        ingredients[num] = {
            'name': recipe_ing.ingredient.name,
            'value': recipe_ing.amount,
            'units': recipe_ing.ingredient.units
        }
        num += 1
    return ingredients


def get_ingredients_from_post(post_req):
    ingredients = {}
    ing_names = {}
    if not post_req:
        return ingredients

    for key, val in post_req.items():
        if key.startswith('nameIngredient'):
            # print(key, val)
            num = key.split('_')[1]

            # Объединение одинаковых ингредиентов списка
            curr_ing_name = post_req[f'nameIngredient_{num}']
            if curr_ing_name in ing_names:
                print('old: ', ingredients[ing_names[curr_ing_name]]['value'])
                print('add: ', post_req[f'valueIngredient_{num}'])
                ingredients[ing_names[curr_ing_name]]['value'] = str(
                    Decimal(ingredients[ing_names[curr_ing_name]]['value'].replace(',', '.')) +
                    Decimal(str(post_req[f'valueIngredient_{num}']))#.replace(',', '.'))
                )
                continue
            # Новый ингредиент в списке
            ingredients[num] = {
                'name': curr_ing_name,
                'value': post_req[f'valueIngredient_{num}'],
                'units': post_req[f'unitsIngredient_{num}'],
            }
            ing_names.update({curr_ing_name: num })
            # ing_obj = get_object_or_404(Ingredient, name=val)
    return ingredients


def save_recipe(request, form, recipe, ingredients):
    if recipe:
        form.save(commit=False)
    else:
        recipe = form.save(commit=False)
        recipe.author = request.user

    recipe.slug = decode_slugify(recipe.name)
    recipe.save()
    ri_objs = []
    for num, ing in ingredients.items():
        ingredient = get_object_or_404(Ingredient, name=ing['name'])
        print(num, ' new: ', ing['value'])
        ri_objs.append(RecipeIngredients(
            recipe=recipe,
            ingredient=ingredient,
            amount=str(Decimal(ing['value'].replace(',', '.')))
        ))
        print(num, ' new: ', ing['value'])
    RecipeIngredients.objects.bulk_create(ri_objs)
    form.save_m2m()
    return recipe


def prepare_and_save_recipe(request, form, recipe, ingredients):
    try:
        with transaction.atomic():
            if recipe:
                recipe.recipeingredients.all().delete()
            return save_recipe(request, form, recipe, ingredients)

    except IntegrityError:
        raise HttpResponseBadRequest


def get_purchases_count(request):
    if request.user.is_authenticated:
        return request.user.purchases.count()
    # Здесь будет неавторизованный юзер
    return 0