from django import forms

from .models import Recipe, RecipeIngredients, RecipeTag
from .utils import get_ingredients_from_post


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'image', 'description', 'cooking_time', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise forms.ValidationError('Укажите теги!')
        return tags

    def clean(self):
        ingredients = get_ingredients_from_post(self.data)
        if not ingredients:
            raise forms.ValidationError('Укажите ингредиенты!')
        return self.cleaned_data
