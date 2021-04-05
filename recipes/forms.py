from django import forms #import ModelForm, ValidationError, ChoiceWidget

from .models import Recipe, RecipeIngredients


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'image', 'author', 'text', 'cooking_time', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            #ChoiceWidget(            ),
        }