from django import forms #import ModelForm, ValidationError, ChoiceWidget

from .models import Recipe, RecipeIngredients
from .utils import get_ingredients


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'image', 'description', 'cooking_time', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Recipe.objects.filter(name=name).exists():
            raise forms.ValidationError('Такое название уже существует!')
        return name
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise forms.ValidationError('Укажите теги!')
        return tags

    def clean(self):
        ingredients = get_ingredients(self.data)
        print('check ingredients..')
        if not ingredients:
            raise forms.ValidationError('Укажите ингредиенты!')
        return self.cleaned_data
