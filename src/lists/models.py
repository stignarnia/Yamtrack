from django.conf import settings
from django.db import models
from django.db.models import Q


class Item(models.Model):
    """Model for items in custom lists."""

    media_id = models.PositiveIntegerField()
    media_type = models.CharField(max_length=12)
    title = models.CharField(max_length=255)
    image = models.URLField()
    season_number = models.PositiveIntegerField(null=True)
    episode_number = models.PositiveIntegerField(null=True)

    class Meta:
        """Meta options for the model."""

        unique_together = ["media_id", "media_type", "season_number", "episode_number"]
        ordering = ["media_id"]

    def __str__(self):
        """Return the name of the item."""
        name = self.title
        if self.season_number:
            name += f" S{self.season_number}"
            if self.episode_number:
                name += f"E{self.episode_number}"
        return name


class CustomListManager(models.Manager):
    """Manager for custom lists."""

    def get_user_lists(self, user):
        """Return the custom lists that the user owns or collaborates on."""
        return (
            self.filter(
                Q(owner=user) | Q(collaborators=user),
            )
            .prefetch_related(
                "items",
                "collaborators",
            )
            .distinct()
        )


class CustomList(models.Model):
    """Model for custom lists."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collaborated_lists",
        blank=True,
    )
    items = models.ManyToManyField(
        Item,
        related_name="custom_lists",
        blank=True,
        through="CustomListItem",
    )

    objects = CustomListManager()

    class Meta:
        """Meta options for the model."""

        ordering = ["name"]
        unique_together = ["name", "owner"]

    def __str__(self):
        """Return the name of the custom list."""
        return self.name

    @property
    def ordered_items(self):
        """Return the items in the list ordered by date added."""
        return self.items.order_by("-customlistitem__date_added")

    def user_can_edit(self, user):
        """Check if the user can edit the list."""
        return self.owner == user

    def user_can_delete(self, user):
        """Check if the user can delete the list."""
        return self.owner == user


class CustomListItem(models.Model):
    """Model for items in custom lists."""

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    custom_list = models.ForeignKey(CustomList, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the model."""

        ordering = ["date_added"]
        unique_together = ["item", "custom_list"]

    def __str__(self):
        """Return the name of the list item."""
        return self.item.title