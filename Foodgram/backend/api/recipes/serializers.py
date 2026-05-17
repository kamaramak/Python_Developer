"""
Сериализаторы для приложения 'recipes' для моделей:
    - Ingredient,
    - Tag,
    - RecipeIngredient,
    - Recipe.
"""

from django.db import transaction
from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField
from interactions.models import Favorite, ShoppingCart
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

from ..users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")
        read_only_fields = ("id", "measurement_unit")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = ("id", "name", "slug")
        read_only_fields = ("id",)


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Сериализатор на запись для модели RecipeIngredient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение для модели RecipeIngredient."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit",
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор на запись для модели Recipe."""

    ingredients = RecipeIngredientWriteSerializer(
        many=True,
        write_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate(self, attrs):
        if "ingredients" not in attrs:
            raise serializers.ValidationError(
                "Требуется указать хотя бы 1 ингредиент!"
            )
        if "tags" not in attrs:
            raise serializers.ValidationError(
                "Требуется указать хотя бы 1 тег!"
            )
        return attrs

    def validate_ingredients(self, value):
        """
        Валидация поля ingredients:
        - Содержится как минимум 1 ингредиент;
        - Нет повторяющихся ингредиентов.
        """
        if not value:
            raise serializers.ValidationError(
                "Требуется указать хотя бы 1 ингредиент!"
            )
        unique_ingredients = {i["id"] for i in value}
        if len(unique_ingredients) < len(value):
            raise serializers.ValidationError(
                "Указаны повторяющиеся ингредиенты!"
            )
        return value

    def validate_tags(self, value):
        """
        Валидация поля tags:
            - Содержится как минимум 1 тег;
            - Нет повторяющихся тегов.
        """
        if not value:
            raise serializers.ValidationError(
                "Требуется указать хотя бы 1 тег!"
            )
        unique_tags = set(value)
        if len(unique_tags) < len(value):
            raise serializers.ValidationError("Указаны повторяющиеся теги!")
        return value

    def _set_ingredients_and_tags(self, recipe, tags, ingredients):
        """Приватный метод для создания/обновления тегов и ингредиентов."""
        if tags is not None:
            recipe.tags.set(tags)
        if ingredients is not None:
            recipe.recipe_ingredients.all().delete()
            RecipeIngredient.objects.bulk_create(
                [
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient["id"],
                        amount=ingredient["amount"],
                    )
                    for ingredient in ingredients
                ]
            )

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)
        tags = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        self._set_ingredients_and_tags(instance, tags, ingredients)
        return instance

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        user = self.context["request"].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        self._set_ingredients_and_tags(recipe, tags, ingredients)
        return recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор на чтениедля модели Recipe."""

    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        source="recipe_ingredients", many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.ImageField(
        allow_empty_file=False,
    )
    tags = TagSerializer(
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        """Возвращает True если рецепт в избранном у текущего пользователя."""
        request = self.context.get("request")
        return (
            request
            and request.user.is_authenticated
            and Favorite.objects.filter(user=request.user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """
        Возвращает True если рецепт в списке покупок текущего пользователя.
        """
        request = self.context.get("request")
        return (
            request
            and request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )
