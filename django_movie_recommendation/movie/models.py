from common.models import BaseModel
from django.db import models
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
        blank=True,
        through='MovieBelongsToPlatform',
    )
    advices = models.ManyToManyField(
        UserCustom,
        related_name='recommend_movies',
        blank=True,
        through='recommendation.UserRecommendMovie',
    )

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
    )

    def __str__(self):
        return f'{self.pk} - {self.name}'


class MovieBelongsToPlatform(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.movie.title} | {self.platform.name}'
