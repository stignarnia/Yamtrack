# Generated by Django 5.1.1 on 2024-10-26 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_anime_item_alter_game_item_alter_manga_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='source',
            field=models.CharField(choices=[('tmdb', 'tmdb'), ('mal', 'mal'), ('mangaupdates', 'mangaupdates'), ('igdb', 'igdb'), ('manual', 'manual')], max_length=20),
        ),
    ]
