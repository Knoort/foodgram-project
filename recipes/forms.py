from django import forms
from decimal import Decimal, InvalidOperation

from .models import Recipe
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

    def clean_cooking_time(self):
        time = self.cleaned_data['cooking_time']
        if not str(time).isdigit():
            raise forms.ValidationError('Неправильное время приготовления!')
        if not int(time) > 0:
            raise forms.ValidationError(
                'Время приготовления должно быть положительным!'
            )
        return time

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
