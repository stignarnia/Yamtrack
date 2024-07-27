# Generated by Django 5.0.6 on 2024-07-25 21:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_anime_item_episode_item_game_item_manga_item_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ['related_season', 'item']},
        ),
        migrations.AlterUniqueTogether(
            name='anime',
            unique_together={('item', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together={('related_season', 'item')},
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('item', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='manga',
            unique_together={('item', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together={('item', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together={('related_tv', 'item')},
        ),
        migrations.AlterUniqueTogether(
            name='tv',
            unique_together={('item', 'user')},
        ),
        migrations.RemoveField(
            model_name='anime',
            name='image',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='title',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='episode_number',
        ),
        migrations.RemoveField(
            model_name='game',
            name='image',
        ),
        migrations.RemoveField(
            model_name='game',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='game',
            name='title',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='image',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='title',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='image',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='title',
        ),
        migrations.RemoveField(
            model_name='season',
            name='image',
        ),
        migrations.RemoveField(
            model_name='season',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='season',
            name='season_number',
        ),
        migrations.RemoveField(
            model_name='season',
            name='title',
        ),
        migrations.RemoveField(
            model_name='tv',
            name='image',
        ),
        migrations.RemoveField(
            model_name='tv',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='tv',
            name='title',
        ),
    ]
