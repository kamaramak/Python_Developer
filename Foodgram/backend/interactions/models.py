"""
Модели приложения interactions:
    - Favorite,
    - ShoppingCart.
"""

from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    """Модель для работы с избранными рецептами."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь в избранном",
        related_name="favorite_recipes",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт в избранном",
        related_name="favorite_users",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["user", "recipe"],
            ),
        ]

    def __str__(self):
        return f"{self.recipe} в избранном пользователя {self.user}"


class ShoppingCart(models.Model):
    """Модель для работы со списком покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь в списке покупок",
        related_name="shopping_cart",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт в избранном",
        related_name="shopping_cart_by",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["user", "recipe"],
            ),
        ]

    def __str__(self):
        return f"{self.recipe} в списке покупок пользователя {self.user}"
