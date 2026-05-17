"""Кастомные фильтры, используемые в проекте."""

from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import ModelMultipleChoiceFilter

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    """
    Фильтрация ингредиентов по полю 'name':
        - по вхождению в начале названия;
        - по вхождению в произвольном месте названия.
    """

    name = CharFilter(method="filter_name")

    class Meta:
        model = Ingredient
        fields = ["name"]

    def filter_name(self, queryset, name, value):
        """Фильтр по названию ингредиента."""
        current_queryset = queryset.filter(name__istartswith=value)
        if not current_queryset:
            return queryset.filter(name__icontains=value)
        return current_queryset


class RecipeFilter(FilterSet):
    """
    Фильтрация рецептов по полям
    ['author', 'tags', 'is_favorited', 'is_in_shopping_cart'].
    """

    is_favorited = CharFilter(method="filter_is_favorited")
    is_in_shopping_cart = CharFilter(method="filter_is_in_shopping_cart")
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ["is_favorited", "is_in_shopping_cart", "author", "tags"]

    def filter_is_favorited(self, queryset, name, value):
        """Отображение рецептов, добвленных в избранное текущим юзером."""
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if value == "1":
            return queryset.filter(favorite_users__user=user)
        return queryset.exclude(favorite_users__user=user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Отображение рецептов, добвленных в список покупок текущим юзером."""
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if value == "1":
            return queryset.filter(shopping_cart_by__user=user)
        return queryset.exclude(shopping_cart_by__user=user)
