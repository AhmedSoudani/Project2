from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("items/<int:listing_id>", views.items, name="items"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.showlists, name="showlists"),
    path("add_comment/<int:item_id>/", views.add_comment, name="add_comment"),
    path("endbid/<int:item_id>/", views.endbid, name="endbid")
]
