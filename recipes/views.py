from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError, connection, reset_queries
from django.http import HttpResponseBadRequest
from django.forms import ValidationError
# from django.utils.text import slugify
from django.contrib.auth import get_user_model

# from uuslug import slugify
from decimal import Decimal
from .models import Recipe, TagChoices
from .forms import RecipeForm
from foodgram.settings import PAGINATION_PAGE_SIZE


from .models import Ingredient, RecipeIngredients, RecipeTag
from .utils import get_ingredients, decode_slugify

User = get_user_model()
TAGS = [name[0] for name in TagChoices.choices]

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


def index(request, author_username=None):
    all_tags = RecipeTag.objects.all()
    tags_checked = request.GET.getlist('tags', [])
    reset_queries()
    print(tags_checked)
    recipes = Recipe.objects.filter(
        tags__name__in=(tags_checked if tags_checked else TAGS)
        ).select_related(
            'author'
        # ).prefetch_related(
            # 'tags', 'ingredients'
    ).distinct()
    page_title = 'Рецепты'

    if author_username:
        recipes = recipes.filter(author__username=author_username)
        author = get_object_or_404(User, username=author_username)
        if author.first_name or author.last_name:
            page_title = f'{author.first_name} {author.last_name}'
        else:
            page_title = f'{author.username}'

    paginator = Paginator(recipes, PAGINATION_PAGE_SIZE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    # print(connection.queries)
    context = {
        'author_username': author_username,
        'page_title': page_title,
        'all_tags': all_tags,
        'tags_checked': tags_checked,
        'recipes': recipes,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'index.html', context)


#@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    all_tags = RecipeTag.objects.all()
    # all_tag_ids = [str(tag.id) for tag in all_tags]
    # tags_checked = request.POST.getlist('tags', [])#all_tag_ids)
    print('POST tags: ', request.POST.getlist('tags', 'no tags'))
    ingredients = get_ingredients(request.POST)
    print('getted:', ingredients)

    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)

    context = {
        'form': form,
        'all_tags': all_tags,
        # 'tags_checked': tags_checked,
        'ingredients': ingredients
    }
    return render(request, 'formRecipe.html', context)


def edit_recipe(request, recipe_id, slug):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    print('POST tags: ', request.POST.getlist('tags', 'no tags'))
    if (request.user != recipe.author) and not request.user.is_superuser:
        return redirect('recipe_view_redirect', recipe_id=recipe.id)
    pass
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    all_tags = RecipeTag.objects.all()
    context = {
        'form': form,
        'all_tags': all_tags,
        # 'ingredients': ingredients
    }
    return render(request, 'formRecipe.html', context)


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    reset_queries()
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),#.prefetch_related('ingredients'),
        id=recipe_id,
        slug=slug
    )
    recipe_ings = recipe.recipeingredients.select_related('ingredient')
    # print(recipe.tags.values()) #prefetch_related('recipe'))
    # print(connection.queries)
    context = {
        'recipe': recipe,
        'recipe_ings': recipe_ings
    }
    return render(request, 'singlePage.html', context)