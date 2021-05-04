from django import forms #import ModelForm, ValidationError, ChoiceWidget
from django.core.files.storage import FileSystemStorage

from .models import Recipe, RecipeIngredients, RecipeTag
from .utils import get_ingredients_from_post


class RecipeForm(forms.ModelForm):
    # tags = forms.ModelMultipleChoiceField(
    #     label='Теги',
    #     queryset=RecipeTag.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )
    class Meta:
        model = Recipe
        fields = ['name', 'image', 'description', 'cooking_time', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        print(image)
        print(self.files)
        form_file = self.files.get('image')
        if form_file:
            fs = FileSystemStorage()
            form_file_name = fs.save('tempimage', form_file)
            form_file_url = fs.url(form_file_name)
            temp_file = fs.path(form_file_name)
            print (form_file_url)
        return image

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise forms.ValidationError('Укажите теги!')
        return tags

    def clean(self):
        fs = FileSystemStorage()
        fs.delete('tempimage')
        ingredients = get_ingredients_from_post(self.data)
        print('check ingredients..')
        if not ingredients:
            raise forms.ValidationError('Укажите ингредиенты!')
        return self.cleaned_data
