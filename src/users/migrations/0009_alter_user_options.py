# Generated by Django 5.0.6 on 2024-07-02 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0008_user_game_layout_alter_user_last_search_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
    ]
