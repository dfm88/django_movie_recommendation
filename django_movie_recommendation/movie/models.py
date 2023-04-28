from common.models import BaseModel
from django.db import models
from django.utils.text import slugify
from user.models import UserCustom

"""MOVIE"""


class MovieGenreChoice(models.TextChoices):
    ACTION = "ACTION", "ACTION"
    COMEDY = "COMEDY", "COMEDY"
    DRAMA = "DRAMA", "DRAMA"
    HORROR = "HORROR", "HORROR"
    THRILLER = "THRILLER", "THRILLER"
    OTHER = "OTHER", "OTHER"


class Movie(BaseModel):
    title = models.CharField(max_length=31, unique=True)
    slug_title = models.SlugField(max_length=31, unique=True)
    genre = models.CharField(
        max_length=15,
        choices=MovieGenreChoice.choices,
        default=MovieGenreChoice.OTHER,
    )
    watchers = models.ManyToManyField(
        UserCustom,
        related_name='watched_movies',
        blank=True,
        through='UserWatchedMovie',
    )
    platforms = models.ManyToManyField(
        'Platform',
        related_name='movies',
    )
    advices = models.ManyToManyField(
        UserCustom,
        related_name='recommend_movies',
        blank=True,
        through='recommendation.UserRecommendMovie',
    )

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk} - {self.title}:{self.genre}'


class UserWatchedMovie(BaseModel):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.pk} - {self.user.username} | {self.movie.title}'


"""PLATFORM"""


class MoviePlatformChoice(models.TextChoices):
    AMAZON_PRIME = "AMAZON_PRIME", "AMAZON_PRIME"
    NETFLIX = "NETFLIX", "NETFLIX"
    DISNEY_PLUS = "DISNEY_PLUS", "DISNEY_PLUS"
    OTHER = "OTHER", "OTHER"


class Platform(BaseModel):
    name = models.CharField(
        max_length=15,
        choices=MoviePlatformChoice.choices,
        default=MoviePlatformChoice.OTHER,
        unique=True,
    )

    def __str__(self):
        return f'{self.pk} - {self.name}'
