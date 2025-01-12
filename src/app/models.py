import datetime
import logging

from django.conf import settings
from django.core.validators import (
    DecimalValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import CheckConstraint, Max, Q, Sum, UniqueConstraint
from django.urls import reverse
from model_utils import FieldTracker
from simple_history.models import HistoricalRecords
from simple_history.utils import bulk_create_with_history, bulk_update_with_history

from app.providers import services, tmdb
from app.templatetags.app_extras import slug

logger = logging.getLogger(__name__)

MEDIA_TYPES = ["movie", "tv", "season", "episode", "anime", "manga", "game"]
READABLE_MEDIA_TYPES = {
    "movie": "Movie",
    "tv": "TV Show",
    "season": "Season",
    "episode": "Episode",
    "anime": "Anime",
    "manga": "Manga",
    "game": "Game",
}

STATUS_IN_PROGRESS = "In progress"
STATUS_COMPLETED = "Completed"
STATUS_REPEATING = "Repeating"
STATUS_PLANNING = "Planning"
STATUS_PAUSED = "Paused"
STATUS_DROPPED = "Dropped"

SOURCES = ["tmdb", "mal", "mangaupdates", "igdb", "manual"]


class Item(models.Model):
    """Model for items in custom lists."""

    media_id = models.PositiveIntegerField()
    source = models.CharField(
        max_length=20,
        choices=[(source, source) for source in SOURCES],
    )
    media_type = models.CharField(
        max_length=10,
        choices=[
            (media_type, READABLE_MEDIA_TYPES[media_type]) for media_type in MEDIA_TYPES
        ],
        default="movie",
    )
    title = models.CharField(max_length=255)
    image = models.URLField()
    season_number = models.PositiveIntegerField(null=True, blank=True)
    episode_number = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        """Meta options for the model."""

        constraints = [
            UniqueConstraint(
                fields=["media_id", "source", "media_type"],
                condition=Q(season_number__isnull=True, episode_number__isnull=True),
                name="unique_item_without_season_episode",
            ),
            UniqueConstraint(
                fields=["media_id", "source", "media_type", "season_number"],
                condition=Q(season_number__isnull=False, episode_number__isnull=True),
                name="unique_item_with_season",
            ),
            UniqueConstraint(
                fields=[
                    "media_id",
                    "source",
                    "media_type",
                    "season_number",
                    "episode_number",
                ],
                condition=Q(season_number__isnull=False, episode_number__isnull=False),
                name="unique_item_with_season_episode",
            ),
            CheckConstraint(
                check=Q(
                    media_type="season",
                    season_number__isnull=False,
                    episode_number__isnull=True,
                )
                | ~Q(media_type="season"),
                name="season_number_required_for_season",
            ),
            CheckConstraint(
                check=Q(
                    media_type="episode",
                    season_number__isnull=False,
                    episode_number__isnull=False,
                )
                | ~Q(media_type="episode"),
                name="season_and_episode_required_for_episode",
            ),
            CheckConstraint(
                check=Q(
                    ~Q(media_type__in=["season", "episode"]),
                    season_number__isnull=True,
                    episode_number__isnull=True,
                )
                | Q(media_type__in=["season", "episode"]),
                name="no_season_episode_for_other_types",
            ),
        ]
        ordering = ["media_id"]

    def __str__(self):
        """Return the name of the item."""
        name = self.title
        if self.season_number:
            name += f" S{self.season_number}"
            if self.episode_number:
                name += f"E{self.episode_number}"
        return name

    @classmethod
    def generate_manual_id(cls):
        """Generate a new ID for manual items."""
        return (
            cls.objects.filter(source="manual")
            .exclude(
                Q(media_type__in=["season", "episode"]),
            )
            .count()
            + 1
        )

    @property
    def url(self):
        """Return the URL of the item."""
        if self.media_type in ["season", "episode"]:
            return reverse(
                "season_details",
                kwargs={
                    "source": self.source,
                    "media_id": self.media_id,
                    "title": slug(self.title),
                    "season_number": self.season_number,
                },
            )
        return reverse(
            "media_details",
            kwargs={
                "source": self.source,
                "media_type": self.media_type,
                "media_id": self.media_id,
                "title": slug(self.title),
            },
        )

    @property
    def event_color(self):
        """Return the color of the item for the calendar."""
        colors = {
            "anime": "#0d6efd",  # blue
            "manga": "#dc3545",  # red
            "game": "#d63384",  # pink
            "tv": "#198754",  # green
            "season": "#6f42c1",  # purple
            "episode": "#6610f2",  # indigo
            "movie": "#fd7e14",  # orange
        }
        return colors[self.media_type]

    @property
    def media_type_readable(self):
        """Return the readable media type."""
        return READABLE_MEDIA_TYPES[self.media_type]


class Media(models.Model):
    """Abstract model for all media types."""

    history = HistoricalRecords(
        cascade_delete_history=True,
        inherit=True,
        excluded_fields=[
            "item",
            "user",
            "related_tv",
        ],
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=1,
        validators=[
            DecimalValidator(3, 1),
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    progress = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=12,
        default=STATUS_COMPLETED,
        choices=[
            (STATUS_COMPLETED, STATUS_COMPLETED),
            (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS),
            (STATUS_REPEATING, STATUS_REPEATING),
            (STATUS_PLANNING, STATUS_PLANNING),
            (STATUS_PAUSED, STATUS_PAUSED),
            (STATUS_DROPPED, STATUS_DROPPED),
        ],
    )
    repeats = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    class Meta:
        """Meta options for the model."""

        abstract = True
        ordering = ["-score"]
        unique_together = ["item", "user"]

    def __str__(self):
        """Return the title of the media."""
        return self.item.__str__()

    def save(self, *args, **kwargs):
        """Save the media instance."""
        if "progress" in self.tracker.changed():
            self.process_progress()

        if "status" in self.tracker.changed():
            self.process_status()

        super().save(*args, **kwargs)

    def process_progress(self):
        """Update fields depending on the progress of the media."""
        if self.progress < 0:
            self.progress = 0
        else:
            max_progress = services.get_media_metadata(
                self.item.media_type,
                self.item.media_id,
                self.item.source,
            )["max_progress"]

            if max_progress:
                self.progress = min(self.progress, max_progress)

                if self.progress == max_progress:
                    self.status = STATUS_COMPLETED

    def process_status(self):
        """Update fields depending on the status of the media."""
        if self.status == STATUS_COMPLETED:
            if not self.end_date:
                self.end_date = datetime.datetime.now(tz=settings.TZ).date()

            max_progress = services.get_media_metadata(
                self.item.media_type,
                self.item.media_id,
                self.item.source,
            )["max_progress"]

            if max_progress:
                self.progress = max_progress

            if self.tracker.previous("status") == STATUS_REPEATING:
                self.repeats += 1

        elif self.status == STATUS_IN_PROGRESS and not self.start_date:
            self.start_date = datetime.datetime.now(tz=settings.TZ).date()

    def increase_progress(self):
        """Increase the progress of the media by one."""
        self.progress += 1
        self.save()
        logger.info("Watched %s E%s", self, self.progress)

    def decrease_progress(self):
        """Decrease the progress of the media by one."""
        self.progress -= 1
        self.save()
        logger.info("Unwatched %s E%s", self, self.progress + 1)

    def progress_response(self):
        """Return the data needed to update the progress of the media."""
        media_metadata = services.get_media_metadata(
            self.item.media_type,
            self.item.media_id,
            self.item.source,
        )
        response = {"item": self.item}
        max_progress = media_metadata["max_progress"]

        response["progress"] = self.progress
        response["max"] = self.progress == max_progress
        response["min"] = self.progress == 0

        return response


class TV(Media):
    """Model for TV shows."""

    tracker = FieldTracker()

    @tracker  # postpone field reset until after the save
    def save(self, *args, **kwargs):
        """Save the media instance."""
        super(Media, self).save(*args, **kwargs)

        if "status" in self.tracker.changed() and self.status == STATUS_COMPLETED:
            self.completed()

    @property
    def progress(self):
        """Return the total episodes watched for the TV show."""
        return sum(season.progress for season in self.seasons.all())

    @property
    def repeats(self):
        """Return the number of max repeated episodes in the TV show."""
        return max((season.repeats for season in self.seasons.all()), default=0)

    @property
    def start_date(self):
        """Return the date of the first episode watched."""
        return min(
            (season.start_date for season in self.seasons.all()),
            default=datetime.date(datetime.MINYEAR, 1, 1),
        )

    @property
    def end_date(self):
        """Return the date of the last episode watched."""
        return max(
            (season.end_date for season in self.seasons.all()),
            default=datetime.date(datetime.MINYEAR, 1, 1),
        )

    def completed(self):
        """Create remaining seasons and episodes for a TV show."""
        tv_metadata = services.get_media_metadata(
            self.item.media_type,
            self.item.media_id,
            self.item.source,
        )
        max_progress = tv_metadata["max_progress"]

        if not max_progress or self.progress > max_progress:
            return

        seasons_to_update = []
        episodes_to_create = []

        season_numbers = [
            season["season_number"]
            for season in tv_metadata["related"]["seasons"]
            if season["season_number"] != 0
        ]
        tv_with_seasons_metadata = services.get_media_metadata(
            "tv_with_seasons",
            self.item.media_id,
            self.item.source,
            season_numbers,
        )
        for season_number in season_numbers:
            season_metadata = tv_with_seasons_metadata[f"season/{season_number}"]

            item, _ = Item.objects.get_or_create(
                media_id=self.item.media_id,
                source=self.item.source,
                media_type="season",
                season_number=season_number,
                defaults={
                    "title": self.item.title,
                    "image": season_metadata["image"],
                },
            )
            try:
                season_instance = Season.objects.get(
                    item=item,
                    user=self.user,
                )

                if season_instance.status != STATUS_COMPLETED:
                    season_instance.status = STATUS_COMPLETED
                    seasons_to_update.append(season_instance)

            except Season.DoesNotExist:
                season_instance = Season(
                    item=item,
                    score=None,
                    status=STATUS_COMPLETED,
                    notes="",
                    related_tv=self,
                    user=self.user,
                )
                Season.save_base(season_instance)
            episodes_to_create.extend(
                season_instance.get_remaining_eps(season_metadata),
            )
        bulk_update_with_history(seasons_to_update, Season, ["status"])
        bulk_create_with_history(episodes_to_create, Episode)


class Season(Media):
    """Model for seasons of TV shows."""

    related_tv = models.ForeignKey(
        TV,
        on_delete=models.CASCADE,
        related_name="seasons",
    )

    tracker = FieldTracker()

    class Meta:
        """Limit the uniqueness of seasons.

        Only one season per media can have the same season number.
        """

        unique_together = ["related_tv", "item"]

    def __str__(self):
        """Return the title of the media and season number."""
        return f"{self.item.title} S{self.item.season_number}"

    @tracker  # postpone field reset until after the save
    def save(self, *args, **kwargs):
        """Save the media instance."""
        # if related_tv is not set
        if self.related_tv_id is None:
            self.related_tv = self.get_tv()

        super(Media, self).save(*args, **kwargs)

        if "status" in self.tracker.changed() and self.status == STATUS_COMPLETED:
            season_metadata = services.get_media_metadata(
                "season",
                self.item.media_id,
                self.item.source,
                [self.item.season_number],
            )
            bulk_create_with_history(
                self.get_remaining_eps(season_metadata),
                Episode,
            )

    @property
    def progress(self):
        """Return the total episodes watched for the season."""
        return self.episodes.count()

    @property
    def current_episode(self):
        """Return the current episode of the season."""
        # continue initial watch
        if self.status == STATUS_IN_PROGRESS:
            sorted_episodes = sorted(
                self.episodes.all(),
                key=lambda e: e.item.episode_number,
                reverse=True,
            )
        else:
            # sort by repeats and then by episode_number
            sorted_episodes = sorted(
                self.episodes.all(),
                key=lambda e: (e.repeats, e.item.episode_number),
                reverse=True,
            )

        if sorted_episodes:
            return sorted_episodes[0]
        return None

    @property
    def repeats(self):
        """Return the number of max repeated episodes in the season."""
        return max((episodes.repeats for episodes in self.episodes.all()), default=0)

    @property
    def start_date(self):
        """Return the date of the first episode watched."""
        return min(
            (episode.watch_date for episode in self.episodes.all()),
            default=datetime.date(datetime.MINYEAR, 1, 1),
        )

    @property
    def end_date(self):
        """Return the date of the last episode watched."""
        return max(
            (episode.watch_date for episode in self.episodes.all()),
            default=datetime.date(datetime.MINYEAR, 1, 1),
        )

    def increase_progress(self):
        """Watch the next episode of the season."""
        current_episode = self.current_episode
        season_metadata = services.get_media_metadata(
            "season",
            self.item.media_id,
            self.item.source,
            [self.item.season_number],
        )
        episodes = season_metadata["episodes"]

        if current_episode:
            next_episode_number = tmdb.find_next_episode(
                current_episode.item.episode_number,
                episodes,
            )
        else:
            # start watching from the first episode
            next_episode_number = episodes[0]["episode_number"]

        today = datetime.datetime.now(tz=settings.TZ).date()

        if next_episode_number:
            self.watch(next_episode_number, today)
        else:
            logger.info("No more episodes to watch.")

    def watch(self, episode_number, watch_date):
        """Create or add a repeat to an episode of the season."""
        item = self.get_episode_item(episode_number)

        try:
            episode = Episode.objects.get(
                related_season=self,
                item=item,
            )
            episode.watch_date = watch_date
            episode.repeats += 1
            episode.save()
            logger.info(
                "%s rewatched successfully.",
                episode,
            )
        except Episode.DoesNotExist:
            # from the form, watch_date is a string
            if watch_date == "None":
                watch_date = None

            episode = Episode.objects.create(
                related_season=self,
                item=item,
                watch_date=watch_date,
            )
            logger.info(
                "%s created successfully.",
                episode,
            )

    def decrease_progress(self):
        """Unwatch the current episode of the season."""
        episode_number = self.current_episode.item.episode_number
        self.unwatch(episode_number)

    def unwatch(self, episode_number):
        """Unwatch the episode instance."""
        try:
            item = self.get_episode_item(episode_number)

            episode = Episode.objects.get(
                related_season=self,
                item=item,
            )

            if episode.repeats > 0:
                episode.repeats -= 1
                episode.save(update_fields=["repeats"])
                logger.info(
                    "%s watch count decreased.",
                    episode,
                )
            else:
                episode.delete()
                logger.info(
                    "%s deleted successfully.",
                    episode,
                )

        except Episode.DoesNotExist:
            logger.warning(
                "Episode %sE%s does not exist.",
                self,
                episode_number,
            )

    def progress_response(self):
        """Return the data needed to update the progress of the season."""
        media_metadata = services.get_media_metadata(
            self.item.media_type,
            self.item.media_id,
            self.item.source,
            [self.item.season_number],
        )
        response = {"item": self.item}
        max_progress = media_metadata["max_progress"]

        response["current_episode"] = self.current_episode
        if self.current_episode:
            response["max"] = self.current_episode.item.episode_number == max_progress
            response["min"] = False
        else:
            response["max"] = False
            response["min"] = True

        return response

    def get_tv(self):
        """Get related TV instance for a season and create it if it doesn't exist."""
        try:
            tv = TV.objects.get(
                item__media_id=self.item.media_id,
                item__media_type="tv",
                item__season_number=None,
                item__source=self.item.source,
                user=self.user,
            )
        except TV.DoesNotExist:
            tv_metadata = services.get_media_metadata(
                "tv",
                self.item.media_id,
                self.item.source,
            )

            # creating tv with multiple seasons from a completed season
            if (
                self.status == STATUS_COMPLETED
                and tv_metadata["details"]["number_of_seasons"] > 1
            ):
                status = STATUS_IN_PROGRESS
            else:
                status = self.status

            item, _ = Item.objects.get_or_create(
                media_id=self.item.media_id,
                source="tmdb",
                media_type="tv",
                defaults={
                    "title": tv_metadata["title"],
                    "image": tv_metadata["image"],
                },
            )

            tv = TV.objects.create(
                item=item,
                score=None,
                status=status,
                notes="",
                user=self.user,
            )

            logger.info("%s did not exist, it was created successfully.", tv)

        return tv

    def get_remaining_eps(self, season_metadata):
        """Return episodes needed to complete a season."""
        max_episode_number = Episode.objects.filter(related_season=self).aggregate(
            max_episode_number=Max("item__episode_number"),
        )["max_episode_number"]

        if max_episode_number is None:
            max_episode_number = 0

        episodes_to_create = []
        today = datetime.datetime.now(tz=settings.TZ).date()

        # Create Episode objects for the remaining episodes
        for episode in reversed(season_metadata["episodes"]):
            if episode["episode_number"] <= max_episode_number:
                break

            item = self.get_episode_item(episode["episode_number"], season_metadata)

            episode_db = Episode(
                related_season=self,
                item=item,
                watch_date=today,
            )
            episodes_to_create.append(episode_db)

        return episodes_to_create

    def get_episode_item(self, episode_number, season_metadata=None):
        """Get the episode item instance, create it if it doesn't exist."""
        if not season_metadata:
            season_metadata = services.get_media_metadata(
                "season",
                self.item.media_id,
                self.item.source,
                [self.item.season_number],
            )

        image = settings.IMG_NONE
        for episode in season_metadata["episodes"]:
            if episode["episode_number"] == episode_number:
                if episode.get("still_path"):
                    image = f"http://image.tmdb.org/t/p/original{episode['still_path']}"
                else:
                    image = episode["image"]
                break

        item, _ = Item.objects.get_or_create(
            media_id=self.item.media_id,
            source=self.item.source,
            media_type="episode",
            season_number=self.item.season_number,
            episode_number=episode_number,
            defaults={
                "title": self.item.title,
                "image": image,
            },
        )

        return item


class Episode(models.Model):
    """Model for episodes of a season."""

    history = HistoricalRecords(
        cascade_delete_history=True,
        excluded_fields=["item", "related_season"],
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    related_season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="episodes",
    )
    watch_date = models.DateField(null=True, blank=True)
    repeats = models.PositiveIntegerField(default=0)

    class Meta:
        """Limit the uniqueness of episodes.

        Only one episode per season can have the same episode number.
        """

        unique_together = ["related_season", "item"]
        ordering = ["related_season", "item"]

    def __str__(self):
        """Return the season and episode number."""
        return self.item.__str__()

    def save(self, *args, **kwargs):
        """Save the episode instance."""
        super().save(*args, **kwargs)

        if self.related_season.status in (STATUS_IN_PROGRESS, STATUS_REPEATING):
            season_number = self.item.season_number
            tv_with_seasons_metadata = services.get_media_metadata(
                "tv_with_seasons",
                self.item.media_id,
                self.item.source,
                [season_number],
            )
            season_metadata = tv_with_seasons_metadata[f"season/{season_number}"]
            max_progress = len(season_metadata["episodes"])
            total_repeats = self.related_season.episodes.aggregate(
                total_repeats=Sum("repeats"),
            )["total_repeats"]

            total_watches = self.related_season.progress + total_repeats

            if total_watches >= max_progress * (self.related_season.repeats + 1):
                self.related_season.status = STATUS_COMPLETED
                self.related_season.save_base(update_fields=["status"])

                last_season = tv_with_seasons_metadata["related"]["seasons"][-1][
                    "season_number"
                ]
                # mark the TV show as completed if it's the last season
                if season_number == last_season:
                    self.related_season.related_tv.status = STATUS_COMPLETED
                    self.related_season.related_tv.save_base(update_fields=["status"])


class Manga(Media):
    """Model for manga."""

    tracker = FieldTracker()


class Anime(Media):
    """Model for anime."""

    tracker = FieldTracker()


class Movie(Media):
    """Model for movies."""

    tracker = FieldTracker()


class Game(Media):
    """Model for games."""

    tracker = FieldTracker()

    def increase_progress(self):
        """Increase the progress of the media by 30 minutes."""
        self.progress += 30
        self.save()
        logger.info("Watched %s E%s", self, self.progress)

    def decrease_progress(self):
        """Decrease the progress of the media by 30 minutes."""
        self.progress -= 30
        self.save()
        logger.info("Unwatched %s E%s", self, self.progress + 1)
