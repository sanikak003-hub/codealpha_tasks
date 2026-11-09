from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed_view, name="home"),
    path("feed/", views.feed_view, name="feed"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path("u/<str:username>/", views.profile_view, name="profile"),
    path("posts/create/", views.create_post_view, name="create_post"),
    path("posts/<int:post_id>/like/", views.toggle_like_view, name="toggle_like"),
    path("posts/<int:post_id>/comment/", views.add_comment_view, name="add_comment"),
    path("u/<str:username>/follow/", views.toggle_follow_view, name="toggle_follow"),
]
