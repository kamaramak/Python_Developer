"""
Модели приложения recipes:
    - Tag,
    - Ingredient,
    - Recipe,
    - RecipeIngredient.
"""

import secrets

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core.constants import (
    MAX_HASH_LENGTH,
    MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
    MAX_INGREDIENT_NAME_LENGTH,
    MAX_RECIPE_NAME_LENGTH,
    MAX_TAG_NAME_LENGTH,
    MAX_TAG_SLUG_LENGTH,
)


User = get_user_model()


class Tag(models.Model):
    """Модель для работы с тегами."""

    name = models.CharField(
        max_length=MAX_TAG_NAME_LENGTH,
        verbose_name="Наименование",
    )
    slug = models.SlugField(
        max_length=MAX_TAG_SLUG_LENGTH,
        verbose_name="Идентификатор",
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для работы с ингредиентами."""

    name = models.CharField(
        max_length=MAX_INGREDIENT_NAME_LENGTH,
        verbose_name="Наименование",
    )
    measurement_unit = models.CharField(
        max_length=MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    """Модель для работы с рецептами."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        related_name="recipes",
    )
    name = models.CharField(
        max_length=MAX_RECIPE_NAME_LENGTH,
        verbose_name="Название",
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        help_text="Время приготовления блюда (в минутах).",
        validators=[MinValueValidator(1)],
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="Изображение",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Промежуточная таблица для связи между рецептами и ингредиентами."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name="Ингредиент",
        related_name="recipe_ingredients",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["recipe", "ingredient"],
            ),
        ]

    def __str__(self):
        return (
            f"{self.ingredient.name} ({self.ingredient.measurement_unit}) "
            f"- {self.amount}"
        )


class ShortLink(models.Model):
    """Модель для работы с короткими ссылками на рецепты."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
        related_name="short_link",
    )
    hash = models.CharField(
        max_length=MAX_HASH_LENGTH,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.generate_hash()
        super().save(*args, **kwargs)

    def generate_hash(self):
        """Генерация хэша для использования в короткой ссылке."""
        while True:
            hash_link = secrets.token_urlsafe(MAX_HASH_LENGTH)[
                :MAX_HASH_LENGTH
            ]
            if not ShortLink.objects.filter(hash=hash_link).exists():
                return hash_link

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["recipe", "hash"],
            ),
        ]

    def __str__(self):
        return f"Short link to {self.recipe}"
