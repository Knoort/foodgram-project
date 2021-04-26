from datetime import datetime

from django.db import models
# from autoslug import AutoSlugField
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name='Название'
        )
    units = models.CharField(
        max_length=20,
        blank=False,
        verbose_name='Ед. изм.'
    )
    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f'{self.name}, {self.units}'


class TagChoices(models.TextChoices):
    BREAKFAST = 'breakfast', 'morning meal'
    LUNCH = 'lunch', 'noon meal'
    DINNER = 'dinner', 'evening meal'


class RecipeTag(models.Model):

    name = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
        choices=TagChoices.choices,
        verbose_name='Тип приема пищи'
    )
    display_name = models.CharField(
        'Имя тега для шаблона',
        max_length=50
    )
    color = models.CharField(
        'Цвет тега',
        max_length=20,
        blank=False,
#        verbose_name='Цвет тега'
    )

    class Meta:
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name='Название рецепта'
        )
    image = models.ImageField('Изображение', upload_to='recipes/')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        blank=True
    )
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время приготовления')
    slug = models.SlugField(
        max_length=50,
        auto_created=True,
        allow_unicode=True
    )
    tags = models.ManyToManyField('RecipeTag', blank=True, related_name='recipes')
    pub_date = models.DateTimeField(
        'Дата публикации',
        null=True,
        db_index=True,
        default=datetime.now()
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients'
    )
    amount = models.DecimalField( max_digits=6, decimal_places=1)

    class Meta:
        unique_together = 'recipe', 'ingredient'
