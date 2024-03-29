from urllib.parse import urlencode

from django.shortcuts import get_object_or_404, redirect, render, reverse
# from django.http import QueryDict

from django.db.models import Exists, OuterRef
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required

from foodgram.settings import PREVIEWS_COUNT

from .forms import RecipeForm, IngredientForm
from .models import (
    Recipe,
    Ingredient,
    RecipeTag
)
from .utils import (
    get_paginator,
    redirect_with_params,
    get_ingredients_from_post,
    get_ingredients_from_qs,
    prepare_and_save_recipe,
    get_purchases,
    products_list
)
from .context_processors import tags

User = get_user_model()
# TAGS = TagChoices.values все существующие объекты только актуальные из базы
TAGS = RecipeTag.objects.values_list('name')

INDEX = 'index'
AUTHOR_PROF = 'author_profile'
FAVORITES = 'favorites'
SUBSCRIPTIONS = 'subscriptions'
PURCHASES = 'purchases'

PAGES_DATA = {
    INDEX: {
        'name': INDEX,
        'title': 'Рецепты'
    },
    AUTHOR_PROF: {
        'name': AUTHOR_PROF,
        'title': None,
    },
    FAVORITES: {
        'name': FAVORITES,
        'title': 'Избранное'
    },
    SUBSCRIPTIONS: {
        'name': SUBSCRIPTIONS,
        'title': 'Мои подписки'
    },
    PURCHASES: {
        'name': PURCHASES,
        'title': 'Список покупок'
    }
}

user_data = {}


def page_not_found(request, exception):
    # Переменную exception не выводим
    return render(
        request, 'misc/t404.html', {'path': request.path}, status=404
    )


def server_error(request):
    return render(request, "misc/t500.html", status=500)


def redirect_index(request):
    return redirect(f'recipes:{INDEX}')


def recipes_set(request, author_username=None, page_choice=None):
    page_data = PAGES_DATA[page_choice]

    tags_checked = tags(request)['tags']['checked']
    recipes = Recipe.objects.filter(
        tags__name__in=(tags_checked if tags_checked else TAGS)
    ).select_related(
        'author'
    ).prefetch_related(
        'admirers'
    ).distinct()

    if request.user.is_authenticated:
        favorites = recipes.filter(admirers__user=request.user)
        recipes = recipes.annotate(
            in_favorites=Exists(favorites.filter(pk__exact=OuterRef('pk')))
        )

    purchases = get_purchases(request)
    recipes = recipes.annotate(
        in_purchases=Exists(purchases.filter(pk__exact=OuterRef('pk')))
    )

    if page_choice == AUTHOR_PROF:
        author = get_object_or_404(User, username=author_username)
        print(author.get_all_permissions())
        recipes = recipes.filter(author=author)
        page_data['author'] = author
        if request.user.is_authenticated:
            page_data['following'] = author.follower.filter(
                user=request.user
            ).exists()
        else:
            page_data['following'] = False

    elif page_choice == FAVORITES:
        if request.user.is_authenticated:
            recipes = recipes.filter(pk__in=favorites.values('pk'))
        else:
            return redirect(f'recipes:{INDEX}')

    try:
        page, paginator = get_paginator(request, recipes)
    except Exception:
        return redirect_with_params(request, page='1')

    context = {
        'page_data': page_data,
        'recipes': recipes,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'index.html', context)


def purchases(request, download=False):
    purchases = get_purchases(request)

    if download:
        return products_list(purchases)

    context = {
        'page_data': PAGES_DATA[PURCHASES],
        'recipes': purchases,
    }
    return render(request, 'shopList.html', context)


def get_purchases_count(request):
    return get_purchases(request).count()


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return redirect(
        'recipes:recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
    )


def recipe_view_slug(request, recipe_id, slug):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),
        id=recipe_id,
        slug=slug
    )
    recipe_ings = recipe.recipeingredients.select_related('ingredient')
    if request.user.is_authenticated:
        following = recipe.author.follower.filter(user=request.user)
        is_favorite = recipe.admirers.filter(user=request.user)
    else:
        following = False
        is_favorite = False

    in_purchases = recipe in get_purchases(request)
    context = {
        'recipe': recipe,
        'recipe_ings': recipe_ings,
        'following': following,
        'is_favorite': is_favorite,
        'in_purchases': in_purchases
    }
    return render(request, 'singlePage.html', context)


@login_required
def subscriptions(request):
    page_data = PAGES_DATA[SUBSCRIPTIONS]
    page_data['previews_cnt'] = PREVIEWS_COUNT
    authors = User.objects.filter(
        follower__user=request.user
    ).prefetch_related(
        'recipes'
    )
    try:
        page, paginator = get_paginator(request, authors)
    except Exception:
        return redirect_with_params(request, page='1')

    context = {
        'page_data': page_data,
        'authors': authors,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'myFollow.html', context)


@login_required
def delete_recipe(request, recipe_id=None, confirm=None):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if confirm:
        recipe.delete()
        return redirect(f'recipes:{INDEX}')
    return render(request, 'deleteRecipeConfirm.html', {'recipe': recipe})


@login_required
def new_edit_recipe(request, recipe_id=None, slug=None):
    print('in, GET', request.GET)
    print('in, POST', request.POST)
    if 'edit_ingredients' in request.POST:
        ings = get_ingredients_from_post(request.POST)
        recipe_ings_names = [ing['name'] for ing in ings.values()]

        if request.user not in user_data:
            user_data.update({request.user: {}})
        user_data[request.user][f'edited_ings_{recipe_id}'] = ings
        print(user_data[request.user])

        url = reverse('recipes:recipe_ings')
        return redirect_with_params(
            request,
            url,
            ings=recipe_ings_names,
            recipe_id=recipe_id
        )
    # print(request.user.groups.all().values_list('pk', 'name'))
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    ) if recipe_id else None

    # Если попытка редактирования не автором и не суперюзером, то отбой
    if (
        recipe and
        (request.user != recipe.author) and
        not request.user.is_superuser
    ):
        return redirect('recipes:recipe_view_redirect', recipe_id=recipe.id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    # возврат из редактирования ингредиентов
    if (
        'ingredients_edited' in request.GET and
        request.user in user_data and
        f'edited_ings_{recipe_id}' in user_data[request.user]
    ):
        ingredients = user_data[request.user].pop(
            f'edited_ings_{recipe_id}'
        )
        print('edited, OK', ingredients)
    elif recipe and not request.POST:
        # Редактирование рецепта - 1 открытие формы.
        ingredients = get_ingredients_from_qs(
            recipe.recipeingredients.all()
        )
        print('recipe, not POST', ingredients)
    else:
        # Создание рецепта или повторная отправка формы.
        ingredients = get_ingredients_from_post(request.POST)
        print('not recipe or POST', ingredients)

    if form.is_valid():
        recipe = prepare_and_save_recipe(request, form, recipe, ingredients)
        return redirect('recipes:recipe_view_redirect', recipe_id=recipe.id)

    context = {
        'recipe': recipe,
        'form': form,
        'ingredients': ingredients,
    }
    return render(request, 'formRecipe.html', context)


@permission_required(
    'recipes.add_ingredient',
    'recipes.view_ingredient',
    'recipes.change_recipeingredients'
)
def recipe_ings(request):
    # print('ings, GET',request.GET)
    # print('ings, POST',request.POST)
    recipe_id = request.GET.get('recipe_id', '')
    if recipe_id.isdigit():
        recipe = get_object_or_404(
            Recipe,
            id=int(recipe_id)
        )
    else:
        recipe = None

    recipe_ings = request.GET.getlist('ings', [])
    ing_edit = request.GET.get('edit', None)
    ing_edit = int(ing_edit) if ing_edit and ing_edit.isdigit() else None

    ings = Ingredient.objects.filter(name__in=recipe_ings)
    for ing in ings:
        ing.link = (
            urlencode({'ings': recipe_ings}, doseq=True) + '&' +
            urlencode({
                'edit': ing.pk,
                'recipe_id': recipe_id
            })
        )
    context = {
        'recipe': recipe,
        'ings': ings
    }
    if not ing_edit:
        return render(request, 'IngredientsList.html', context)

    ing = get_object_or_404(Ingredient, pk=ing_edit)
    form = IngredientForm(
        request.POST or None,
        instance=ing
    )
    if request.POST and form.is_valid():
        form.save()
        # print('save, GET',request.GET)
        # print('save, POST',request.POST)
        url = reverse('recipes:recipe_ings')
        return redirect_with_params(
            request,
            url,
            ings=recipe_ings,
            recipe_id=recipe_id
        )

    context.update({'form': form})
    # print('edit, GET',request.GET)
    # print('edit, POST',request.POST)
    return render(request, 'IngredientsList.html', context)
