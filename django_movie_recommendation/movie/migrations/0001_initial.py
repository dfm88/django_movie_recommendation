# Generated by Django 4.2 on 2023-04-28 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=31, unique=True)),
                ("slug_title", models.SlugField(max_length=31, unique=True)),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("ACTION", "ACTION"),
                            ("COMEDY", "COMEDY"),
                            ("DRAMA", "DRAMA"),
                            ("HORROR", "HORROR"),
                            ("THRILLER", "THRILLER"),
                            ("OTHER", "OTHER"),
                        ],
                        default="OTHER",
                        max_length=15,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Platform",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("AMAZON_PRIME", "AMAZON_PRIME"),
                            ("NETFLIX", "NETFLIX"),
                            ("DISNEY_PLUS", "DISNEY_PLUS"),
                            ("OTHER", "OTHER"),
                        ],
                        default="OTHER",
                        max_length=15,
                        unique=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserWatchedMovie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movie.movie"
                    ),
                ),
            ],
        ),
    ]
