from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction, IntegrityError, connection, reset_queries
from django.http import HttpResponseBadRequest
from django.forms import ValidationError
# from django.utils.text import slugify

# from uuslug import slugify
from decimal import Decimal
from .models import Recipe
from .forms import RecipeForm


from .models import Ingredient, RecipeIngredients, RecipeTag
from .utils import get_ingredients, decode_slugify

#@transaction.atomic
def save_recipe(request, form):
    recipe = form.save(commit=False)
    recipe.author = request.user
    print(request.user, recipe.author)
    try:
        with transaction.atomic():
            recipe.slug = decode_slugify(recipe.name)
            recipe.save()
            ri_objs = []
            ingredients = get_ingredients(request.POST)
            print('save:', ingredients)
            for num, ing in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=ing['name'])
                ri_objs.append(RecipeIngredients(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=Decimal(ing['value'].replace(',', '.'))
                ))
            RecipeIngredients.objects.bulk_create(ri_objs)
            form.save_m2m()
            return recipe

    except IntegrityError:
        raise HttpResponseBadRequest


#@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    print(request.POST)
    all_tags = RecipeTag.objects.all()
    tags_checked = [int(tag) for tag in request.POST.getlist('tags', [])]

    ingredients = get_ingredients(request.POST)
    print('getted:', ingredients)

    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)

    # if not ingredients:
    #     form.add_error(None, ValidationError('Укажите ингредиенты!'))
    print() 
    for field in form:
        # print(field.name, field.value())
            # print(field)
        pass

    context = {
        'form': form,
        'all_tags': all_tags,
        'tags_checked': tags_checked,
        'ingredients': ingredients
    }
    # print(form.order_fields('tags'))
    return render(request, 'formRecipe.html', context)


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    reset_queries()
    recipe = get_object_or_404(
        Recipe.objects.select_related('author').prefetch_related('ingredients'),
        id=recipe_id,
        slug=slug
    )
    author = recipe.author
    print(author)
    recipe_ings = recipe.recipeingredients.all()
    # print(recipe.tags.values()) #prefetch_related('recipe'))
    print(recipe_ings.values())
    # print(connection.queries)

    context = {
        'recipe': recipe,
        'author': author,
        'recipe_ings': recipe_ings
    }
    return render(request, 'singlePage.html', context)