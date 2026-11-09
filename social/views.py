from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ProfileForm, RegisterForm, UserUpdateForm
from .models import Comment, Follow, Post, Profile


def _safe_post_redirect(request, fallback_name):
    target = request.POST.get("next", "")
    if target and url_has_allowed_host_and_scheme(
        target,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(target)
    return redirect(fallback_name)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.create(user=user)
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("feed")

    return render(request, "social/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Welcome back!")
        return redirect("feed")

    return render(request, "social/login.html", {"form": form})


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def feed_view(request):
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("likes", "comments__author")
        .all()
    )
    for post in posts:
        post.is_liked = post.likes.filter(pk=request.user.pk).exists()
        post.comment_list = post.comments.select_related("author").all()[:5]
        post.comment_count = post.comments.count()

    post_form = None
    return render(request, "social/feed.html", {"posts": posts})


@require_POST
@login_required
def create_post_view(request):
    content = request.POST.get("content", "").strip()
    if not content:
        messages.error(request, "Please write something before publishing.")
    elif len(content) > 2000:
        messages.error(request, "Your post must be 2,000 characters or fewer.")
    else:
        Post.objects.create(author=request.user, content=content)
        messages.success(request, "Your post has been published.")
    return redirect("feed")


@require_POST
@login_required
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return _safe_post_redirect(request, "feed")


@require_POST
@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    content = request.POST.get("content", "").strip()
    if not content:
        messages.error(request, "A comment cannot be empty.")
    elif len(content) > 500:
        messages.error(request, "Your comment must be 500 characters or fewer.")
    else:
        Comment.objects.create(post=post, author=request.user, content=content)
    return _safe_post_redirect(request, "feed")


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)

    posts = Post.objects.filter(author=profile_user).select_related("author").prefetch_related("likes")
    for post in posts:
        post.is_liked = post.likes.filter(pk=request.user.pk).exists()

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    is_following = (
        Follow.objects.filter(follower=request.user, following=profile_user).exists()
        if request.user != profile_user
        else False
    )

    return render(
        request,
        "social/profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "posts": posts,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
        },
    )


@login_required
def edit_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, instance=profile)

    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile", username=request.user.username)

    return render(
        request,
        "social/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@require_POST
@login_required
def toggle_follow_view(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("profile", username=username)

    relation, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user,
    )
    if created:
        messages.success(request, f"You are now following {target_user.username}.")
    else:
        relation.delete()
        messages.info(request, f"You unfollowed {target_user.username}.")

    return redirect("profile", username=username)
