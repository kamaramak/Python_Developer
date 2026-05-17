"""Представления для приложения 'interactions'"""

import io
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from interactions.models import Favorite, ShoppingCart
from recipes.models import Recipe, RecipeIngredient

from ..users.serializers import RecipeInPostSerializer
from .serializers import FavoriteSerializer, ShoppingCartSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """Представление для модели Favorite."""

    serializer_class = FavoriteSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["post", "delete"]
    pagination_class = None

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs.get("pk")
        # Проверка на существование рецепта, добавляемого в избранное
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {"recipe": recipe.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return_serializer = RecipeInPostSerializer(recipe)
        headers = self.get_success_headers(return_serializer.data)
        return Response(
            return_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get("pk"))
        instance = Favorite.objects.filter(user=request.user, recipe=recipe)
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Вы не добавили в избранное этот рецепт!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Представление для модели ShoppingCart."""

    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ["post", "delete"]
    pagination_class = None

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs.get("pk")
        # Проверка на существование рецепта, добавляемого в избранное
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {"recipe": recipe.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return_serializer = RecipeInPostSerializer(recipe)
        headers = self.get_success_headers(return_serializer.data)
        return Response(
            return_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get("pk"))
        instance = ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        )
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Вы не добавили в список покупок этот рецепт!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    """Функция для отправки файла со списком покупок."""
    timestamp = datetime.now().strftime("%d-%m-%Y")
    shopping_cart_file = generate_shopping_cart_file(request.user, timestamp)
    file = io.BytesIO(shopping_cart_file.encode("utf-8"))
    file.seek(0)
    response = HttpResponse(
        file.getvalue(), content_type="text/plain; charset=utf-8"
    )
    return response


def generate_shopping_cart_file(user, timestamp):
    """Функция для генерации текста списка покупок."""
    rows = [f"🛒 СПИСОК ПОКУПОК ({timestamp})"]
    ingredients = (
        RecipeIngredient.objects.filter(recipe__shopping_cart_by__user=user)
        .values("ingredient__name", "ingredient__measurement_unit")
        .annotate(total_amount=Sum("amount"))
        .order_by("ingredient__name")
    )
    for count, ingredient in enumerate(ingredients, start=1):
        name = ingredient["ingredient__name"]
        measurement_unit = ingredient["ingredient__measurement_unit"]
        amount = ingredient["total_amount"]
        rows.append(f"{count}) {name} - {amount} ({measurement_unit})")
    return "\n".join(rows)
