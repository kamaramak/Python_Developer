"""Настройка админ-зоны проекта."""

from django.contrib import admin

from interactions.models import Favorite

from .models import Ingredient, Recipe, RecipeIngredient, ShortLink, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ-зона для модели Ingredient."""

    list_display = ("id", "name", "measurement_unit")
    list_editable = ("name", "measurement_unit")
    list_filter = ("measurement_unit",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ-зона для модели Tag."""

    list_display = ("id", "name", "slug")
    list_editable = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ-зона для модели Recipe."""

    list_display = (
        "id",
        "author",
        "name",
        "cooking_time",
        "display_count_favorited",
    )
    list_editable = (
        "name",
        "cooking_time",
    )
    search_fields = (
        "author",
        "name",
    )

    def display_count_favorited(self, obj):
        """Отображение количества добавлений рецепта в избранное."""
        return Favorite.objects.filter(recipe=obj).count()

    display_count_favorited.short_description = (
        "Количество добавлений в избранное"
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админ-зона для модели RecipeIngredient."""

    list_display = (
        "recipe",
        "ingredient",
        "amount",
    )


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    """Админ-зона для модели ShortLink."""

    list_display = (
        "recipe",
        "hash",
    )
