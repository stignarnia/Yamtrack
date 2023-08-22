import asyncio
import logging

import requests
from app.models import Anime, Manga, User
from app.utils import helpers
from decouple import config

MAL_API = config("MAL_API", default="")
logger = logging.getLogger(__name__)


def mal_data(username: str, user: User) -> None:
    """Import anime and manga from MyAnimeList."""

    logger.info("Importing %s from MyAnimeList", username)

    header = {"X-MAL-CLIENT-ID": MAL_API}
    anime_url = f"https://api.myanimelist.net/v2/users/{username}/animelist?fields=list_status{{comments}}&nsfw=true&limit=1000"
    animes = get_whole_response(anime_url, header)

    bulk_add_anime = add_media_list(animes, "anime", user)

    manga_url = f"https://api.myanimelist.net/v2/users/{username}/mangalist?fields=list_status{{comments}}&nsfw=true&limit=1000"
    mangas = get_whole_response(manga_url, header)

    bulk_add_manga = add_media_list(mangas, "manga", user)

    Anime.objects.bulk_create(bulk_add_anime, ignore_conflicts=True)
    Manga.objects.bulk_create(bulk_add_manga, ignore_conflicts=True)

    logger.info("Finished importing %s from MyAnimeList", username)


def get_whole_response(url: str, header: dict) -> dict:
    """Fetch whole data from user.

    Continues to fetch data from the next URL until there is no more data to fetch.
    """
    response = requests.get(url, headers=header, timeout=5)
    data = response.json()

    # usually when username not found
    if response.status_code == 404:  # noqa: PLR2004
        error_message = data.get("error")
        raise ValueError(error_message)

    while "next" in data["paging"]:
        next_url = data["paging"]["next"]
        # Fetch the data from the next URL
        next_data = requests.get(next_url, headers=header, timeout=5).json()
        # Append the new data to the existing data in the data
        data["data"].extend(next_data["data"])
        # Update the "paging" key with the new "next" URL (if any)
        data["paging"] = next_data["paging"]

    return data


def add_media_list(response: dict, media_type: str, user: User) -> list:
    """Add media to list for bulk creation."""

    bulk_media = []
    bulk_images = []
    media_mapping = helpers.media_type_mapper(media_type)

    for content in response["data"]:
        status = get_status(content["list_status"]["status"])

        if media_type == "anime":
            progress = content["list_status"]["num_episodes_watched"]
        else:
            progress = content["list_status"]["num_chapters_read"]

        if "main_picture" in content["node"]:
            image_url = content["node"]["main_picture"]["large"]
            bulk_images.append(image_url)

            image_filename = helpers.get_image_filename(image_url, media_type)
        else:
            image_filename = "none.svg"

        instance = media_mapping["model"](
            user=user,
            title=content["node"]["title"],
            image=image_filename,
        )

        form = media_mapping["form"](
            data={
                "media_id": content["node"]["id"],
                "media_type": media_type,
                "score": content["list_status"]["score"],
                "progress": progress,
                "status": status,
                "start_date": content["list_status"].get("start_date", None),
                "end_date": content["list_status"].get("finish_date", None),
                "notes": content["list_status"]["comments"],
            },
            instance=instance,
            post_processing=False,
        )

        if form.is_valid():
            bulk_media.append(form.instance)
        else:
            error_message = (
                f"Error importing {content['node']['title']}: {form.errors.as_data()}"
            )
            logger.error(error_message)

    asyncio.run(helpers.images_downloader(bulk_images, media_type))

    return bulk_media


def get_status(status: str) -> str:
    """Convert the status from MyAnimeList to the status used in the app."""

    switcher = {"plan_to_watch": "Planning", "on_hold": "Paused", "reading": "Watching"}
    return switcher.get(status, status.capitalize())