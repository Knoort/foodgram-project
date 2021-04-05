# Generated by Django 3.1.5 on 2021-04-05 13:44

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': ('рецепт',), 'verbose_name_plural': 'рецепты'},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
        migrations.AddField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2021, 4, 5, 16, 42, 54, 927940), null=True, verbose_name='Дата публикации'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='display_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, verbose_name='Имя тега для шаблона'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, through='recipes.RecipeIngredients', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='recipetag',
            name='color',
            field=models.CharField(max_length=20, verbose_name='Цвет тега'),
        ),
    ]