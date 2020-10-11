"""
Connects url paths, methods from views.py, and related names.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("listing/<str:listing_id>/<str:user_id>", views.listing_page, name="listing_page"),
    path("watch", views.watch, name="watch"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_listing/<str:category>", views.category_listing, name="category_listing"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close")
]
