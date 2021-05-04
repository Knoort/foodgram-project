from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db import connection, reset_queries #, transaction
# from django.utils.text import slugify
from django.contrib.auth import get_user_model

# from uuslug import slugify
from .models import Recipe, TagChoices
from .forms import RecipeForm
from foodgram.settings import PAGINATION_PAGE_SIZE, PREVIEWS_COUNT


from .models import Ingredient, RecipeIngredients, RecipeTag
from .utils import (
    get_ingredients_from_post,
    get_ingredients_from_qs,
    prepare_and_save_recipe
)

User = get_user_model()
TAGS = [name[0] for name in TagChoices.choices]

INDEX = 'index'
AUTHOR_PROF = 'author_profile'
FAVORITES = 'favorites'
SUBSCRIPTIONS = 'subscriptions'

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
    }
}
#@transaction.atomic

def recipes_set(request, author_username=None, page_choice=None):
    all_tags = RecipeTag.objects.all()
    tags_checked = request.GET.getlist('tags', [])
    reset_queries()
    recipes = Recipe.objects.filter(
        tags__name__in=(tags_checked if tags_checked else TAGS)
        ).select_related(
            'author'
        ).prefetch_related(
            'admirers'
        ).distinct()
    favorites = recipes.filter(admirers__user=request.user)
    page_data = PAGES_DATA[page_choice]

    if page_choice == AUTHOR_PROF:
        author = get_object_or_404(User, username=author_username)
        recipes = recipes.filter(author=author)
        page_data['author'] = author
        page_data['following'] = author.follower.filter(
            user=request.user
            ).exists()
    elif page_choice == FAVORITES:
        recipes = favorites #recipes.filter(admirers__user=request.user)


    paginator = Paginator(recipes, PAGINATION_PAGE_SIZE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    print(connection.queries)

    context = {
        'page_data': page_data,
        'all_tags': all_tags,
        'favorites': favorites,
        'tags_checked': tags_checked,
        'recipes': recipes,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'index.html', context)


def subscriptions(request):
    page_data = PAGES_DATA[SUBSCRIPTIONS]
    page_data['previews_cnt'] = PREVIEWS_COUNT
    authors = User.objects.filter(
        follower__user=request.user.id
    ).prefetch_related(
        'recipes'
    )
    # print(authors.values_list('username'))
    paginator = Paginator(authors, PAGINATION_PAGE_SIZE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    context = {
        'page_data': page_data,
        'authors': authors,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'myFollow.html', context)


#@login_required
def new_edit_recipe(request, recipe_id=None, slug=None):
    recipe = get_object_or_404(
        Recipe,id=recipe_id
        ) if recipe_id else None

    # Если редактирование не автором и не суперюзером, то отбой
    if (
        recipe and
        (request.user != recipe.author) and
        not request.user.is_superuser
    ):
        return redirect('recipe_view_redirect', recipe_id=recipe.id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if recipe and not request.POST :
        ingredients = get_ingredients_from_qs(recipe.recipeingredients.all())
    else:
        ingredients = get_ingredients_from_post(request.POST)

    # print('POST tags: ', request.POST.getlist('tags', 'no tags'))

    if form.is_valid():
        recipe = prepare_and_save_recipe(request, form, recipe, ingredients)
        return redirect('recipes:recipe_view_redirect', recipe_id=recipe.id)

    all_tags = RecipeTag.objects.all()
    context = {
        'recipe': recipe,
        'form': form,
        'all_tags': all_tags,
        'ingredients': ingredients
    }
    print(request.POST)
    print(ingredients)
    return render(request, 'formRecipe.html', context)


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return redirect('recipes:recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    reset_queries()
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),#.prefetch_related('ingredients'),
        id=recipe_id,
        slug=slug
    )
    recipe_ings = recipe.recipeingredients.select_related('ingredient')
    following = recipe.author.follower.filter(user=request.user).exists()
    # print(connection.queries)
    context = {
        'recipe': recipe,
        'recipe_ings': recipe_ings,
        'following': following
    }
    return render(request, 'singlePage.html', context)



# def new_recipe(request):
#     form = RecipeForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=None
#     )
#     ingredients = get_ingredients_from_post(request.POST)
#     print('getted:', ingredients)

#     if form.is_valid():
#         recipe = prepare_and_save_recipe(request, form, None, ingredients)
#         return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)

#     all_tags = RecipeTag.objects.all()

#     context = {
#         'form': form,
#         'all_tags': all_tags,
#         'ingredients': ingredients,
#     }
#     return render(request, 'formRecipe.html', context)