"""Настройка админ-зоны проекта."""

from django.contrib import admin

from .models import Favorite, ShoppingCart


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админ-зона для модели Favorite."""

    list_display = ("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ-зона для модели ShoppingCart."""

    list_display = ("user", "recipe")
