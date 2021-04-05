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
    
    def __str__(self):
        return f'{self.name}, {self.units}'


class RecipeTag(models.Model):
    name = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
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


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name='Название'
        )
    image = models.ImageField('Фото', upload_to='recipes/')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        blank=True
    )
    cooking_time = models.PositiveSmallIntegerField()
    slug = models.SlugField(
        max_length=50,
        auto_created=True,
        allow_unicode=True
    )
    tags = models.ManyToManyField(RecipeTag, blank=True, related_name='Блюда')
    pub_date = models.DateTimeField(
        'Дата публикации',
        null=True,
        db_index=True,
        default=datetime.now()
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'рецепт',
        verbose_name_plural = 'рецепты'
    
    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField( max_digits=6, decimal_places=1)

    class Meta:
        unique_together = 'recipe', 'ingredient'
