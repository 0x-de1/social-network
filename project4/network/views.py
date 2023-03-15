from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import json

from .models import User, Post
from .forms import PostForm


def index(request):
    form = PostForm()

    all_posts = Post.objects.all()
    p = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = all_posts.filter(likes=request.user)
        liked_posts = list(liked_posts.values_list("id", flat=True))

        own_posts = all_posts.filter(user=request.user)
        own_posts = list(own_posts.values_list("id", flat=True))

    else:
        liked_posts = False
        own_posts = False

    return render(
        request,
        "network/index.html",
        {
            "form": form,
            "page_obj": page_obj,
            "liked_posts": liked_posts,
            "own_posts": own_posts,
        },
    )


@login_required
def edit_post(request, post_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=400)
    print("2")

    if post.user != request.user:
        return JsonResponse(
            {"error": "Post does not belong to current user"}, status=400
        )
    print("3")

    print(request.body)
    data = json.loads(request.body)
    print(type(data), data)
    content = data["content"]

    if content:
        post.content = content
        post.save()
        print(post)

        return JsonResponse(
            {"message": "Post updated successfully.", "content": content}, status=201
        )
    else:
        print("5")
        return JsonResponse({"error": "Content cannot be empty"}, status=400)


@login_required
def likes(request, post_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    current_user = request.user
    print(request.POST)

    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=400)
    liked = post.likes.filter(username=current_user.username)

    if liked:
        post.likes.remove(current_user)
    else:
        post.likes.add(current_user)
    like_count = post.likes.count()
    return JsonResponse(
        {"message": "Post liked successfully.", "likes": like_count}, status=201
    )


@login_required
def following_posts(request):
    print(request.POST.get("key1"))

    following_list = request.user.following.all()
    user_posts = Post.objects.filter(user__in=following_list)
    p = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = user_posts.filter(likes=request.user)
        liked_posts = list(liked_posts.values_list("id", flat=True))

        own_posts = user_posts.filter(user=request.user)
        own_posts = list(own_posts.values_list("id", flat=True))

    else:
        liked_posts = False
        own_posts = False

    return render(
        request,
        "network/following.html",
        {
            "page_obj": page_obj,
            "liked_posts": liked_posts,
            "own_posts": own_posts,
        },
    )


@login_required
def follow(request, username):
    if request.method == "POST":
        try:
            profile = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.WARNING, "Profile does not exist")
            return redirect("index")

        current_state = request.POST.get("state")
        current_user = get_user(request)
        print(type(profile), current_state, type(current_user))

        if current_state == "followed":
            print(profile.followers.all())
            profile.followers.remove(current_user)
        elif current_state == "not_follow":
            profile.followers.add(current_user)

    return redirect("profile", username=username)


def profile(request, username):
    current_user = request.user
    try:
        profile = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, "Profile does not exist")
        return redirect("index")
    # if own account
    if current_user == profile:
        follower = False
    else:
        try:
            follower = profile.followers.get(username=current_user.username)
        except ObjectDoesNotExist:
            follower = "not_following"
        else:
            follower = "following"

    user_posts = Post.objects.filter(user=profile)
    p = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = user_posts.filter(likes=request.user)
        liked_posts = list(liked_posts.values_list("id", flat=True))

        own_posts = user_posts.filter(user=request.user)
        own_posts = list(own_posts.values_list("id", flat=True))

    else:
        liked_posts = False
        own_posts = False

    # print(following)
    return render(
        request,
        "network/profile_page.html",
        {
            "profile": profile,
            "page_obj": page_obj,
            "follower": follower,
            "liked_posts": liked_posts,
            "own_posts": own_posts,
        },
    )


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

    return redirect("index")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
