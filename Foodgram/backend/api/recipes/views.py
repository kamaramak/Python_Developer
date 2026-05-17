"""Представления для приложения recipes."""

from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.filters import IngredientFilter, RecipeFilter
from core.permissions import IsAuthorOrReadOnly
from recipes.models import Ingredient, Recipe, ShortLink, Tag

from .serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)


class IngredientViewSet(viewsets.ModelViewSet):
    """Просмотр ингредиентов с поиском и фильтрацией."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = IngredientFilter
    search_fields = ("^name",)
    http_method_names = ["get"]
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    """Просмотр тегов с поиском и фильтрацией."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ["get"]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Просмотр и запись рецептов с фильтрацией.
    Доступные методы: get, post, patch, delete.
    """

    SERIALIZERS = {
        "write": RecipeWriteSerializer,
        "read": RecipeReadSerializer,
    }

    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "delete"):
            return self.SERIALIZERS["write"]
        return self.SERIALIZERS["read"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeReadSerializer(
            recipe, context=self.get_serializer_context()
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        return_instance = serializer.save()
        return_serializer = self.SERIALIZERS["read"](
            return_instance, context=self.get_serializer_context()
        )

        return Response(return_serializer.data)


@api_view(["GET"])
def get_short_link(request, pk):
    """Выдача пользователю короткой ссылки на рецепт."""
    recipe = get_object_or_404(Recipe, pk=pk)
    short_link, _ = ShortLink.objects.get_or_create(recipe=recipe)
    short_link_url = request.build_absolute_uri(f"/s/{short_link.hash}")
    return Response({"short-link": short_link_url})


def redirect_short_link(request, hash_link):
    """Перевод с короткой ссылки на рецепт."""
    short_link = get_object_or_404(ShortLink, hash=hash_link)
    return redirect(f"/recipes/{short_link.recipe.id}")
