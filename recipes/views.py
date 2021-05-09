from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db import connection, reset_queries #, transaction
from django.db.models import Exists, OuterRef
# from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# from uuslug import slugify

from foodgram.settings import PAGINATION_PAGE_SIZE, PREVIEWS_COUNT

from .forms import RecipeForm
from .models import (
    TagChoices,
    Recipe,
    Ingredient,
    RecipeIngredients,
    RecipeTag
)
from .utils import (
    get_ingredients_from_post,
    get_ingredients_from_qs,
    prepare_and_save_recipe,
    get_purchases_count
)

User = get_user_model()
TAGS = TagChoices.values

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


def recipes_set(request, author_username=None, page_choice=None):
    page_data = PAGES_DATA[page_choice]
    page_data['all_tags'] = RecipeTag.objects.all()
    page_data['tags_checked'] = request.GET.getlist('tags', [])

    tags_checked = page_data['tags_checked']
    reset_queries()
    recipes = Recipe.objects.filter(
        tags__name__in=(tags_checked if tags_checked else TAGS)
        ).select_related(
            'author'
        ).prefetch_related(
            'admirers'
        ).distinct()

    if request.user.is_authenticated:
        favorites = recipes.filter(admirers__user=request.user)
        purchases = recipes.filter(purchasers__user=request.user)
        recipes = recipes.annotate(
            in_favorites=Exists(favorites.filter(pk__exact=OuterRef('pk')))
        ).annotate(
            in_purchases=Exists(purchases.filter(pk__exact=OuterRef('pk')))
        )
    else:
        favorites = []
        purchases = []

    if page_choice == AUTHOR_PROF:
        author = get_object_or_404(User, username=author_username)
        recipes = recipes.filter(author=author)
        page_data['author'] = author
        if request.user.is_authenticated:
            page_data['following'] = author.follower.filter(
                user=request.user
                ).exists()
        else:
            page_data['following'] = False

    elif page_choice == FAVORITES:
        if request.user.is_authenticated :
            recipes = recipes.filter(id__in=favorites.values('pk'))
        else:
            return redirect('recipes:index')

    paginator = Paginator(recipes, PAGINATION_PAGE_SIZE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    print(connection.queries)

    context = {
        'page_data': page_data,
        # 'favorites': favorites,
        'purchases_count': get_purchases_count(request),
        'recipes': recipes,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'index.html', context)


@login_required
def subscriptions(request):
    page_data = PAGES_DATA[SUBSCRIPTIONS]
    page_data['previews_cnt'] = PREVIEWS_COUNT
    authors = User.objects.filter(
        follower__user=request.user
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
        'purchases_count': get_purchases_count(request),
        'page': page,
        'paginator': paginator
    }
    return render(request, 'myFollow.html', context)


def purchases(request):
    page_data = PAGES_DATA[PURCHASES]
    recipes = Recipe.objects.filter(purchasers__user__username=request.user.username)
    context = {
        'page_data': page_data,
        'recipes': recipes,
        'purchases_count': recipes.count()
    }
    return render(request, 'shopList.html', context)


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
    following = recipe.author.follower.filter(user__id=request.user.id)
    is_favorite = recipe.admirers.filter(user__id=request.user.id)
    in_purchases = recipe.purchasers.filter(user__id=request.user.id).exists()
    # print(connection.queries)
    context = {
        'recipe': recipe,
        'recipe_ings': recipe_ings,
        'purchases_count': get_purchases_count(request),
        'following': following,
        'is_favorite': is_favorite,
        'in_purchases': in_purchases
    }
    return render(request, 'singlePage.html', context)


@login_required
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
    # Редактирование рецепта - 1 открытие формы.
    if recipe and not request.POST :
        ingredients = get_ingredients_from_qs(recipe.recipeingredients.all())
    # Создание рецепта или повторная отправка формы.
    else:
        ingredients = get_ingredients_from_post(request.POST)

    if form.is_valid():
        recipe = prepare_and_save_recipe(request, form, recipe, ingredients)
        return redirect('recipes:recipe_view_redirect', recipe_id=recipe.id)

    all_tags = RecipeTag.objects.all()
    context = {
        'recipe': recipe,
        'form': form,
        'all_tags': all_tags,
        'ingredients': ingredients,
        'purchases_count': get_purchases_count(request),
    }
    return render(request, 'formRecipe.html', context)
