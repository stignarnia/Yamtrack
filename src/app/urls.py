from django.urls import path, register_converter

from app import converters, views

register_converter(converters.MediaTypeChecker, "media_type")
register_converter(converters.SourceChecker, "source")


urlpatterns = [
    path("", views.home, name="home"),
    path("medialist/<media_type:media_type>", views.media_list, name="medialist"),
    path("search", views.media_search, name="search"),
    path(
        "details/<source:source>/<media_type:media_type>/<int:media_id>/<str:title>",
        views.media_details,
        name="media_details",
    ),
    path(
        "details/<source:source>/tv/<int:media_id>/<str:title>/season/<int:season_number>",
        views.season_details,
        name="season_details",
    ),
    path("track_modal", views.track, name="track"),
    path("progress_edit", views.progress_edit, name="progress_edit"),
    path("media_save", views.media_save, name="media_save"),
    path("media_delete", views.media_delete, name="media_delete"),
    path("episode_handler", views.episode_handler, name="episode_handler"),
    path("create/item", views.create_item, name="create_item"),
    path("create/media", views.create_media, name="create_media"),
    path("history_modal", views.history, name="history"),
    path("history_delete", views.history_delete, name="history_delete"),
]
