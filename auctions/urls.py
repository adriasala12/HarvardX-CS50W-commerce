from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/placebid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category")
]
