
from decimal import Decimal


from django.utils.text import slugify
# from django.utils import encoding
# from django.template import defaultfilters -> slugify
import unidecode
from unidecode import unidecode


def decode_slugify(txt):
    return slugify(unidecode(txt))


def get_ingredients(post_req):
    ingredients = {}
    ing_names = {}
    if not post_req:
        return ingredients

    for key, val in post_req.items():
        if key.startswith('nameIngredient'):
            print(key, val)
            num = key.split('_')[1]

            # Объединение одинаковых ингредиентов списка
            curr_ing_name = post_req[f'nameIngredient_{num}']
            if curr_ing_name in ing_names:
                ingredients[ing_names[curr_ing_name]]['value'] = str(
                    Decimal(ingredients[ing_names[curr_ing_name]]['value']) +
                    Decimal(post_req[f'valueIngredient_{num}'])
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
