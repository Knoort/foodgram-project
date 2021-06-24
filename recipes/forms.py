from django import forms
from decimal import Decimal, InvalidOperation

from .models import Recipe
from .utils import get_ingredients_from_post


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'tags', 'cooking_time', 'description', 'image']

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
        for ing in ingredients.values():
            ing_name = ing['name']
            try:
                ing_amount = Decimal(ing['value'])
            except InvalidOperation:
                raise forms.ValidationError(
                    f'Неверный формат количества ингредиента {ing_name}!'
                )
            except Exception:
                raise forms.ValidationError(
                    f'Что-то не так с количеством ингредиента {ing_name}..'
                )
            if ing_amount <= Decimal('0.0'):
                raise forms.ValidationError(
                    f'{ing_name} - количество ингредиента' +
                    ' должно быть положительным!'
                )
        return self.cleaned_data
