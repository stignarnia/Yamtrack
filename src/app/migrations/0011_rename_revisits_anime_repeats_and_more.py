# Generated by Django 5.0.3 on 2024-04-01 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_anime_revisits_game_revisits_manga_revisits_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='revisits',
            new_name='repeats',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='revisits',
            new_name='repeats',
        ),
        migrations.RenameField(
            model_name='manga',
            old_name='revisits',
            new_name='repeats',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='revisits',
            new_name='repeats',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='revisits',
            new_name='repeats',
        ),
        migrations.RenameField(
            model_name='tv',
            old_name='revisits',
            new_name='repeats',
        ),
    ]
