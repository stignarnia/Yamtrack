import logging
from csv import DictReader

from app import forms
from app.forms import EpisodeForm
from app.models import Episode, Season
from django.apps import apps
from django.core.files.uploadedfile import InMemoryUploadedFile
from users.models import User

logger = logging.getLogger(__name__)


def yamtrack_data(file: InMemoryUploadedFile, user: User) -> None:
    """Import media from CSV file."""

    if not file.name.endswith(".csv"):
        error = "Invalid file format. Please upload a CSV file."
        logger.error(error)
        raise ValueError(error)

    logger.info("Importing from Yamtrack")

    decoded_file = file.read().decode("utf-8").splitlines()
    reader = DictReader(decoded_file)

    bulk_media = {
        "anime": [],
        "manga": [],
        "movie": [],
        "tv": [],
        "season": [],
    }

    episodes = []

    for row in reader:
        media_type = row["media_type"]
        if media_type == "episode":
            form = EpisodeForm(row)
            if form.is_valid():
                episodes.append(
                    {
                        "instance": form.instance,
                        "media_id": row["media_id"],
                        "season_number": row["season_number"],
                    },
                )
            else:
                logger.error(form.errors.as_data())
        else:
            add_bulk_media(row, user, bulk_media)

    # bulk create tv, season, movie, anime and manga
    for media_type, medias in bulk_media.items():
        model = apps.get_model(app_label="app", model_name=media_type)
        model.objects.bulk_create(medias, ignore_conflicts=True)

        logger.info("Imported %s %ss", len(medias), media_type)

    if episodes:
        # bulk create episodes
        for episode in episodes:
            media_id = episode["media_id"]
            season_number = episode["season_number"]
            episode["instance"].related_season = Season.objects.get(
                media_id=media_id,
                season_number=season_number,
                user=user,
            )

        episode_instances = [episode["instance"] for episode in episodes]
        Episode.objects.bulk_create(episode_instances, ignore_conflicts=True)

        logger.info("Imported %s episodes", len(episode_instances))


def add_bulk_media(
    row: dict,
    user: User,
    bulk_media: dict,
) -> None:
    """Add media to list for bulk creation."""

    media_type = row["media_type"]
    model = apps.get_model(app_label="app", model_name=media_type)
    instance = model(user=user, title=row["title"], image=row["image"])

    if media_type == "season":
        instance.season_number = row["season_number"]

    form = forms.get_form_class(media_type)(
        row,
        instance=instance,
        initial={"media_type": media_type},
    )

    if form.is_valid():
        bulk_media[media_type].append(form.instance)
    else:
        logger.error("Error importing %s: %s", row["title"], form.errors.as_data())
