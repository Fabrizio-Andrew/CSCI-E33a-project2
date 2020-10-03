from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<str:listing_name>/<str:user_id>", views.listing_page, name="listing_page"),
    path("watch", views.watch, name="watch"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist")
]
