"""Foodgram API URL конфигурация."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .interactions.views import (
    FavoriteViewSet,
    ShoppingCartViewSet,
    download_shopping_cart,
)
from .recipes.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    get_short_link,
)
from .users.views import FollowViewSet, UserViewSet

app_name = "api"

router = DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("tags", TagViewSet, basename="tags")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("users", UserViewSet, basename="users")

follow_list_viewset = FollowViewSet.as_view({"get": "list"})
follow_detail_viewset = FollowViewSet.as_view(
    {"post": "create", "delete": "destroy"}
)
favorite_viewset = FavoriteViewSet.as_view(
    {"post": "create", "delete": "destroy"}
)
shopping_cart_viewset = ShoppingCartViewSet.as_view(
    {"post": "create", "delete": "destroy"}
)

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path(
        "recipes/download_shopping_cart/",
        download_shopping_cart,
        name="download_shopping_cart",
    ),
    path("recipes/<int:pk>/favorite/", favorite_viewset, name="favorite"),
    path(
        "recipes/<int:pk>/shopping_cart/",
        shopping_cart_viewset,
        name="shopping_cart",
    ),
    path("recipes/<int:pk>/get-link/", get_short_link, name="get_short_link"),
    path(
        "users/subscriptions/",
        follow_list_viewset,
        name="subscriptions_list",
    ),
    path(
        "users/<int:pk>/subscribe/",
        follow_detail_viewset,
        name="subscriptions_detail",
    ),
    path("", include("djoser.urls")),
    path("", include(router.urls)),
]
