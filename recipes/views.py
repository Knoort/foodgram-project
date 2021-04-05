from django.shortcuts import get_object_or_404, redirect, render

from .models import Recipe
from .forms import RecipeForm


from .models import Ingredient, RecipeIngredients


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith():
            pass

def save_recipe(request, form):
    pass



#@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)
    return render(request, 'formRecipe.html', {'form': form})


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.all(), id=recipe_id)
    return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),
        id=recipe_id,
        slug=slug
    )
    return render(request, 'singlePage.html', {'recipe': recipe})