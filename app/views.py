from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    update_session_auth_hash,
    authenticate,
    login as auth_login,
)
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from app.models import Media
from app.forms import UserRegisterForm, UserUpdateForm
from app.utils import api, database


def home(request):
    """Home page"""
    if ("query") in request.POST:
        return redirect(
            "/search/" + request.POST["content"] + "/" + request.POST["query"] + "/"
        )

    elif "score" in request.POST:
        if request.user.is_authenticated:
            database.edit_media(request)
            return redirect("home")

    elif "delete" in request.POST:
        Media.objects.get(
            media_id=request.POST["delete"],
            user=request.user,
            api_origin=request.POST["api_origin"],
        ).delete()
        return redirect("home")

    elif request.user.is_authenticated:
        queryset = Media.objects.filter(user_id=request.user)
        movies = []
        movies_status = {
            "completed": [],
            "planning": [],
            "watching": [],
            "paused": [],
            "dropped": [],
        }
        tv = []
        tv_status = {
            "completed": [],
            "planning": [],
            "watching": [],
            "paused": [],
            "dropped": [],
        }
        anime = []
        anime_status = {
            "completed": [],
            "planning": [],
            "watching": [],
            "paused": [],
            "dropped": [],
        }
        manga = []
        manga_status = {
            "completed": [],
            "planning": [],
            "watching": [],
            "paused": [],
            "dropped": [],
        }

        for media in queryset:
            if media.api_origin == "tmdb":
                if media.media_type == "movie":
                    movies.append(media)
                    movies_status[(media.status).lower()].append(media)

                else:  # media.media_type == "tv"
                    tv.append(media)
                    tv_status[(media.status).lower()].append(media)
            else:  # mal
                if (
                    media.media_type == "anime"
                    or media.media_type == "movie"
                    or media.media_type == "special"
                    or media.media_type == "ova"
                ):
                    anime.append(media)
                    anime_status[(media.status).lower()].append(media)
                else:  # media.media_type == "manga" or media.media_type == "light_novel" or media.media_type == "one_shot"
                    manga.append(media)
                    manga_status[(media.status).lower()].append(media)

        return render(
            request,
            "app/home.html",
            {
                "media": queryset,
                "movies": movies,
                "movies_status": movies_status,
                "tv": tv,
                "tv_status": tv_status,
                "anime": anime,
                "anime_status": anime_status,
                "manga": manga,
                "manga_status": manga_status,
            },
        )

    return render(request, "app/home.html")


def search(request, content, query):
    """Search page"""
    if "query" in request.POST:
        return redirect(
            "/search/" + request.POST["content"] + "/" + request.POST["query"] + "/"
        )

    elif "score" in request.POST:
        if request.user.is_authenticated:
            if Media.objects.filter(
                media_id=request.POST["media_id"],
                user=request.user,
                api_origin=request.POST["api_origin"],
            ).exists():
                database.edit_media(request)
            else:
                database.add_media(request)
        else:
            messages.error(request, "Please log in to track media to your account.")
            return redirect("login")

        return redirect("/search/" + content + "/" + query + "/")

    query_list = api.search(content, query)
    context = {"query_list": query_list}

    if content == "tmdb":
        return render(request, "app/search_tmdb.html", context)
    else:
        return render(request, "app/search_mal.html", context)


def register(request):
    if ("query") in request.POST:
        return redirect(
            "/search/" + request.POST["content"] + "/" + request.POST["query"] + "/"
        )
    elif "username" in request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "app/register.html", {"form": form})


def login(request):
    if ("query") in request.POST:
        return redirect(
            "/search/" + request.POST["content"] + "/" + request.POST["query"] + "/"
        )

    elif "username" in request.POST:
        form = AuthenticationForm()
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(
                request,
                "Please enter a correct username and password. Note that both fields may be case-sensitive.",
            )
    else:
        form = AuthenticationForm()

    return render(request, "app/login.html", {"form": form})


@login_required
def profile(request):
    if "username" in request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password = password_form.save()
            update_session_auth_hash(request, password)
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")
            
    elif "query" in request.POST:
        return redirect(
            "/search/" + request.POST["content"] + "/" + request.POST["query"] + "/"
        )

    elif request.POST.get("mal") and request.POST.get("mal-btn"):
        if api.import_myanimelist(request.POST.get("mal"), request.user):
            messages.success(request, f"Your MyAnimeList has been imported!")
        else:
            messages.error(
                request, "User not found",
            )
        return redirect("profile")

    elif request.FILES.get("tmdb") and request.POST.get("tmdb-btn"):
        if api.import_tmdb(request.FILES.get("tmdb"), request.user):
            messages.success(request, f"Your TMDB list has been imported!")
        else:
            messages.error(request, 'Error importing your list, make sure it\'s a CSV file containing the word "ratings" or "watchlist" in the name')

        return redirect("profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {"user_form": user_form, "password_form": password_form}

    return render(request, "app/profile.html", context)
