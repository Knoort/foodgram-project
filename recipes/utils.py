import os, mimetypes, tempfile

from decimal import Decimal
from pathlib import Path

from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.utils.text import slugify
from unidecode import unidecode

from .models import Ingredient, Recipe, RecipeIngredients


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
            num = key.split('_')[1]

            # Объединение одинаковых ингредиентов списка
            # Имена в списке всегда уникльны
            curr_ing_name = post_req[f'nameIngredient_{num}']
            if curr_ing_name in ing_names:
                # Обращение к полю "количество", добавление к существующему
                ingredients[ing_names[curr_ing_name]]['value'] = str(
                    Decimal(ingredients[ing_names[curr_ing_name]]['value'].replace(',', '.')) +
                    Decimal(str(post_req[f'valueIngredient_{num}']))
                )
                continue
            # Новый ингредиент в списке
            ingredients[num] = {
                'name': curr_ing_name,
                'value': post_req[f'valueIngredient_{num}'],
                'units': post_req[f'unitsIngredient_{num}'],
            }
            ing_names.update({curr_ing_name: num})
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
        ri_objs.append(RecipeIngredients(
            recipe=recipe,
            ingredient=ingredient,
            amount=str(Decimal(ing['value'].replace(',', '.')))
        ))
    RecipeIngredients.objects.bulk_create(ri_objs)
    form.save_m2m()
    return recipe


def prepare_and_save_recipe(request, form, recipe, ingredients):
    try:
        with transaction.atomic():
            if recipe:
                # Если редактируем рецепт - всегда удаляем старые ингредиенты
                recipe.recipeingredients.all().delete()
            return save_recipe(request, form, recipe, ingredients)

    except IntegrityError:
        raise HttpResponseBadRequest


def get_purchases(request):
    if request.user.is_authenticated:
        return Recipe.objects.filter(purchasers__user=request.user)

    purchases_list = request.session.get('purchases')
    if not type(purchases_list) is list:
        purchases_list = []
    purchases = Recipe.objects.filter(pk__in=purchases_list)
    return purchases


def products_list(recipes):
    filename = 'products_list.txt'
    all_ings = {}
    for recipe in recipes:
        for recipe_ing in recipe.recipeingredients.all():
            curr_name = recipe_ing.ingredient.name
            if curr_name in all_ings:
                all_ings[curr_name]['value'] = str(
                    Decimal(all_ings[curr_name]['value']) +
                    Decimal(recipe_ing.amount)
                )
                # В рецепте ингредиенты всегда уникальны
                continue
            all_ings[curr_name] = {
                'value': recipe_ing.amount,
                'units': recipe_ing.ingredient.units
            }
    tpf = tempfile.NamedTemporaryFile(mode='w+')
    fl_path = os.path.join(tempfile.gettempdir(), tpf.name)
    tpf.write("Список продуктов для закупки:\n \n")
    for ing_name, ing in all_ings.items():
        tpf.write(f"{ing_name}: {ing['value']} {ing['units']}" + '\n')
    tpf.seek(0)
    if os.path.exists(fl_path):
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(tpf.read(), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    raise Http404
