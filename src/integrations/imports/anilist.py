import datetime
import logging

from app import forms
from app.models import Anime, Manga
from app.providers import services
from django.apps import apps
from users.models import User

logger = logging.getLogger(__name__)


def importer(username: str, user: User) -> str:
    """Import anime and manga ratings from Anilist."""

    query = """
    query ($userName: String){
        anime: MediaListCollection(userName: $userName, type: ANIME) {
            lists {
                isCustomList
                entries {
                    media{
                        title {
                            userPreferred
                        }
                        coverImage {
                            large
                        }
                        idMal
                    }
                    status
                    score(format: POINT_10_DECIMAL)
                    progress
                    startedAt {
                        year
                        month
                        day
                    }
                    completedAt {
                        year
                        month
                        day
                    }
                    notes
                }
            }
        }
        manga: MediaListCollection(userName: $userName, type: MANGA) {
            lists {
                isCustomList
                entries {
                    media{
                        title {
                            userPreferred
                        }
                        coverImage {
                            large
                        }
                        idMal
                    }
                    status
                    score(format: POINT_10_DECIMAL)
                    progress
                    startedAt {
                        year
                        month
                        day
                    }
                    completedAt {
                        year
                        month
                        day
                    }
                    notes
                }
            }
        }
    }
    """

    variables = {"userName": username}
    url = "https://graphql.anilist.co"

    # dont need to disable cache, as POST requests are not cached
    query = services.api_request(
        url,
        "POST",
        json={"query": query, "variables": variables},
    )

    # returns media that couldn't be added
    return add_media_list(query, warning_message="", user=user)


def add_media_list(query: dict, warning_message: str, user: User) -> str:
    """Add media to list for bulk creation."""

    bulk_media = {"anime": [], "manga": []}

    for media_type in query["data"]:
        logger.info("Importing %ss from Anilist", media_type)

        for status_list in query["data"][media_type]["lists"]:
            if not status_list["isCustomList"]:
                for content in status_list["entries"]:
                    if content["media"]["idMal"] is None:
                        warning_message += (
                            "\n {} ({}): No matching MyAnimeList ID".format(
                                content["media"]["title"]["userPreferred"],
                                media_type.capitalize(),
                            )
                        )
                    else:
                        if content["status"] == "CURRENT":
                            status = "In progress"
                        else:
                            status = content["status"].capitalize()

                        instance = apps.get_model(
                            app_label="app",
                            model_name=media_type,
                        )(
                            user=user,
                            title=content["media"]["title"]["userPreferred"],
                            image=content["media"]["coverImage"]["large"],
                        )
                        form = forms.get_form_class(media_type)(
                            data={
                                "media_id": content["media"]["idMal"],
                                "media_type": media_type,
                                "score": content["score"],
                                "progress": content["progress"],
                                "status": status,
                                "start_date": get_date(content["startedAt"]),
                                "end_date": get_date(content["completedAt"]),
                                "notes": content["notes"],
                            },
                            instance=instance,
                        )
                        if form.is_valid():
                            bulk_media[media_type].append(form.instance)
                        else:
                            warning_message += "\n {} ({}): Import failed".format(
                                content["media"]["title"]["userPreferred"],
                                media_type.capitalize(),
                            )

    Anime.objects.bulk_create(bulk_media["anime"], ignore_conflicts=True)
    Manga.objects.bulk_create(bulk_media["manga"], ignore_conflicts=True)

    return warning_message


def get_date(date: dict) -> datetime.date | None:
    """Return date object from date dict."""

    if date["year"]:
        return datetime.date(date["year"], date["month"], date["day"])

    return None