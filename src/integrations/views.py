"""Contains views for importing and exporting media data from various sources."""

import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST

from integrations import exports, tasks

logger = logging.getLogger(__name__)


@require_POST
def import_mal(request):
    """View for importing anime and manga data from MyAnimeList."""
    username = request.POST["mal"]
    tasks.import_mal.delay(username, request.user)
    messages.success(request, "MyAnimeList import task started in the background.")
    return redirect("profile")


@require_POST
def import_tmdb_ratings(request):
    """View for importing TMDB movie and TV ratings."""
    tasks.import_tmdb.delay(
        request.FILES["tmdb_ratings"],
        request.user,
        "Completed",
    )
    messages.success(request, "TMDB ratings import task started in the background.")
    return redirect("profile")


@require_POST
def import_tmdb_watchlist(request):
    """View for importing TMDB movie and TV watchlist."""
    tasks.import_tmdb.delay(
        request.FILES["tmdb_watchlist"],
        request.user,
        "Planning",
    )
    messages.success(request, "TMDB watchlist import task started in the background.")
    return redirect("profile")


@require_POST
def import_anilist(request):
    """View for importing anime and manga data from AniList."""
    username = request.POST["anilist"]
    tasks.import_anilist.delay(username, request.user)
    messages.success(request, "AniList import task started in the background.")
    return redirect("profile")


@require_POST
def import_kitsu(request):
    """View for importing anime and manga data from Kitsu."""
    username = request.POST["kitsu"]
    tasks.import_kitsu.delay(username, request.user)
    messages.success(request, "Kitsu import task started in the background.")
    return redirect("profile")

@require_POST
def import_yamtrack(request):
    """View for importing anime and manga data from Yamtrack CSV."""
    tasks.import_yamtrack.delay(request.FILES["yamtrack_csv"], request.user)
    messages.success(request, "Yamtrack import task started in the background.")
    return redirect("profile")


@require_GET
def export_csv(request):
    """View for exporting all media data to a CSV file."""
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="yamtrack.csv"'},
    )

    response = exports.db_to_csv(response, request.user)

    logger.info("User %s successfully exported their data", request.user.username)

    return response
