from common.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from movie.models import Movie, Platform
from user.models import UserCustom


class UserRecommendMovie(BaseModel):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    vote = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField()

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.pk} - {self.user.username} | {self.movie.title}'
