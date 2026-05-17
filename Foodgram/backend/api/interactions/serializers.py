"""
Сериализаторы для приложения 'interactions' для моделей:
    - Favorite,
    - ShoppingCart.
"""

from rest_framework import serializers

from interactions.models import Favorite, ShoppingCart
from recipes.models import Recipe


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        model = Favorite
        fields = ("recipe",)

    def validate(self, attrs):
        user = self.context.get("request").user
        recipe = attrs.get("recipe")
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                "Вы уже добавили этот рецепт в избранное!"
            )
        return attrs


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        model = ShoppingCart
        fields = ("recipe",)

    def validate(self, attrs):
        user = self.context.get("request").user
        recipe = attrs.get("recipe")
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                "Вы уже добавили этот рецепт в список покупок!"
            )
        return attrs
