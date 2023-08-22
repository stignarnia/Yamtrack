import csv
import logging

from app.models import TV, Anime, Episode, Manga, Movie, Season, User
from django.db.models.query import QuerySet
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def db_to_csv(response: HttpResponse, user: User) -> HttpResponse:
    """Export a CSV file of the user's media."""

    fields = [
        "media_id",
        "media_type",
        "title",
        "image",
        "score",
        "progress",
        "status",
        "start_date",
        "end_date",
        "notes",
        "season_number",
        "episode_number",
        "watch_date",
    ]

    writer = csv.writer(response, quoting=csv.QUOTE_ALL)
    writer.writerow(fields)

    write_model_to_csv(writer, fields, TV.objects.filter(user=user), "tv")
    write_model_to_csv(writer, fields, Movie.objects.filter(user=user), "movie")
    write_model_to_csv(writer, fields, Season.objects.filter(user=user), "season")
    write_model_to_csv(writer, fields, Episode.objects.filter(related_season__user=user), "episode")  # fmt: skip
    write_model_to_csv(writer, fields, Anime.objects.filter(user=user), "anime")
    write_model_to_csv(writer, fields, Manga.objects.filter(user=user), "manga")

    return response


def write_model_to_csv(writer: csv.writer, fields: list, queryset: QuerySet, media_type: str) -> None:  # fmt: skip
    """Export entries from a model to a CSV file."""

    logger.info("Adding %ss to CSV", media_type)

    for item in queryset:
        # write fields if they exist, otherwise write empty string
        row = [getattr(item, field, "") for field in fields]

        # replace media_type field with the correct value
        row[fields.index("media_type")] = media_type

        if media_type == "episode":
            row[fields.index("media_id")] = item.related_season.media_id
            row[fields.index("title")] = item.related_season.title
            row[fields.index("season_number")] = item.related_season.season_number

        writer.writerow(row)