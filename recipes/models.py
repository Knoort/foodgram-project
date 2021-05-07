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
    BREAKFAST = 'breakfast', 'завтрак'
    LUNCH = 'lunch', 'обед'
    DINNER = 'dinner', 'ужин'


class ColorChoices(models.TextChoices):
    GREEN = 'green', 'зеленый'
    ORANGE = 'orange', 'оранжевый'
    PURPLE = 'purple', 'пурпурный'


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
        choices=ColorChoices.choices,
#        verbose_name='Цвет тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return f'{self._meta.verbose_name} {self.display_name}'
    


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
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
    tags = models.ManyToManyField('RecipeTag', blank=False, related_name='recipes')
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
        related_name='recipeingredients',
        null=True
    )
    amount = models.DecimalField( max_digits=6, decimal_places=1)

    class Meta:
        unique_together = 'recipe', 'ingredient'
        verbose_name = 'Ингредиент рецепта',
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избиратель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='admirers',
        verbose_name='Избранный рецепт'
    )
    
    class Meta:
        unique_together = 'user', 'recipe'
        verbose_name = 'Избранный рецепт',
        verbose_name_plural = 'Избранные'


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Автор'
    )
    
    class Meta:
        unique_together = 'user', 'author'
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'


class Purchases(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchasers',
        verbose_name='рецепт заказа'
    )
    
    class Meta:
        unique_together = 'user', 'recipe'
        verbose_name = 'Закупка',
        verbose_name_plural = 'Закупки'
