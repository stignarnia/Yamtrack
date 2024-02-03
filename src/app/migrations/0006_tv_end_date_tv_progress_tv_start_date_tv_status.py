# Generated by Django 4.2.5 on 2024-02-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_movie_progress"),
    ]

    operations = [
        migrations.AddField(
            model_name="tv",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tv",
            name="progress",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="tv",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tv",
            name="status",
            field=models.CharField(
                choices=[
                    ("Completed", "Completed"),
                    ("In progress", "In progress"),
                    ("Paused", "Paused"),
                    ("Dropped", "Dropped"),
                    ("Planning", "Planning"),
                ],
                default="Completed",
                max_length=12,
            ),
        ),
    ]
