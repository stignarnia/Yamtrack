# Generated by Django 5.0.3 on 2024-04-17 10:41

import django.core.validators
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# app.migrations.0014_historicalanime_historicalepisode_historicalgame_and_more

class Migration(migrations.Migration):

    replaces = [('app', '0001_initial'), ('app', '0002_alter_anime_image_alter_manga_image_and_more'), ('app', '0003_alter_anime_status_alter_manga_status_and_more'), ('app', '0004_movie_start_date'), ('app', '0005_movie_progress'), ('app', '0006_tv_end_date_tv_progress_tv_start_date_tv_status'), ('app', '0007_alter_season_unique_together_remove_tv_end_date_and_more'), ('app', '0008_alter_anime_notes_alter_manga_notes_and_more'), ('app', '0009_game'), ('app', '0010_anime_revisits_game_revisits_manga_revisits_and_more'), ('app', '0011_rename_revisits_anime_repeats_and_more'), ('app', '0012_alter_anime_status_alter_game_status_and_more'), ('app', '0013_alter_episode_options_remove_season_repeats_and_more'), ('app', '0014_historicalanime_historicalepisode_historicalgame_and_more')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('notes', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
            ],
            options={
                'ordering': ['-score'],
                'abstract': False,
                'unique_together': {('media_id', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('repeats', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-score'],
                'abstract': False,
                'unique_together': {('media_id', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('repeats', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-score'],
                'abstract': False,
                'unique_together': {('media_id', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('repeats', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-score'],
                'abstract': False,
                'unique_together': {('media_id', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('progress', models.PositiveIntegerField(default=0)),
                ('repeats', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-score'],
                'abstract': False,
                'unique_together': {('media_id', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('notes', models.TextField(blank=True, default='')),
                ('season_number', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_tv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='app.tv')),
            ],
            options={
                'unique_together': {('related_tv', 'season_number')},
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_number', models.PositiveIntegerField()),
                ('watch_date', models.DateField(blank=True, null=True)),
                ('related_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='app.season')),
                ('repeats', models.PositiveIntegerField(default=0)),
            ],
            options={
                'unique_together': {('related_season', 'episode_number')},
                'ordering': ['related_season', 'episode_number'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalAnime',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('repeats', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical anime',
                'verbose_name_plural': 'historical animes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEpisode',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('watch_date', models.DateField(blank=True, null=True)),
                ('repeats', models.PositiveIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical episode',
                'verbose_name_plural': 'historical episodes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalGame',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('repeats', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical game',
                'verbose_name_plural': 'historical games',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalManga',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('repeats', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical manga',
                'verbose_name_plural': 'historical mangas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalMovie',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('progress', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('repeats', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical movie',
                'verbose_name_plural': 'historical movies',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSeason',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('notes', models.TextField(blank=True, default='')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical season',
                'verbose_name_plural': 'historical seasons',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTV',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.DecimalValidator(3, 1), django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Repeating', 'Repeating'), ('Planning', 'Planning'), ('Paused', 'Paused'), ('Dropped', 'Dropped')], default='Completed', max_length=12)),
                ('notes', models.TextField(blank=True, default='')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical tv',
                'verbose_name_plural': 'historical tvs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
