from distutils.util import strtobool

import django_filters
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from movie.models import Movie

BOOLEAN_CHOICES = (('false', 'False'), ('true', 'True'), ('0', 'False'), ('1', 'True'))


class MovieFilter(django_filters.FilterSet):
    platform = django_filters.CharFilter(field_name='platforms', lookup_expr='name')
    has_watched = django_filters.TypedChoiceFilter(
        method='filter_has_watched', choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    order_by = django_filters.OrderingFilter(
        fields=(('title', 'title'),),
    )

    def filter_has_watched(
        self, queryset: models.QuerySet[Movie], name: str, value: bool
    ):
        return user_has_watched(
            movies=queryset,
            user=self.request.user,
            has_watched=value,
        )

    class Meta:
        model = Movie
        fields = [
            'title',
            'platforms',
            'slug_title',
        ]

    @property
    def qs(self):
        movies = super().qs

        movies = set_watched_switch(
            user=getattr(self.request, 'user', None),
            movies=movies,
        )

        return movies


def user_has_watched(
    movies: models.QuerySet[Movie],
    user: AbstractBaseUser | AnonymousUser | None,
    has_watched: bool,
) -> models.QuerySet[Movie]:
    """Filter queryset by flag getting watched/unwatched movies by user

    Args:
        movies (models.QuerySet[Movie])
        user (AbstractBaseUser | AnonymousUser | None)
        has_watched (bool)

    Returns:
        models.QuerySet[Movie]
    """
    if user and user.is_authenticated:
        filter_ = (
            models.Q(userwatchedmovie__user=user)
            if has_watched
            else (~models.Q(userwatchedmovie__user=user))
        )
        movies = movies.filter(filter_)
    return movies


def set_watched_switch(
    user: AbstractBaseUser | AnonymousUser | None,
    movies: models.QuerySet[Movie],
) -> models.QuerySet[Movie]:
    """Add an additional field 'watched' to be shown in serialization
    to be sent to client depending on whether the user watch the movies or not

    Args:
        user (AbstractBaseUser | AnonymousUser | None)
        movies (models.QuerySet[Movie])

    Returns:
        models.QuerySet[Movie]_
    """
    if user and user.is_authenticated:
        movies = movies.annotate(
            watched=models.Case(
                models.When(userwatchedmovie__user=user, then=models.Value(True)),
                default=models.Value(False),
                output_field=models.BooleanField(),
            )
        )
    return movies


def movie_get(
    request: HttpRequest,
) -> models.QuerySet[Movie]:
    """Get the list of movies based on filters in request object

    Args:
        request (HttpRequest)

    Returns:
        models.QuerySet[Movie]
    """
    mf = MovieFilter(
        data=request.GET,
        queryset=Movie.objects.all(),
        request=request,
    )
    qs = mf.qs
    return qs


def movie_get_one(
    user: AbstractBaseUser | AnonymousUser,
    slug_title: str,
) -> Movie:
    """Get movie by slug_title.
    Add watch boolean for authenticated users

    Args:
        user (AbstractBaseUser | AnonymousUser)
        slug_title (str)

    Returns:
        Movie: _description_
    """
    return get_object_or_404(
        set_watched_switch(
            user=user, movies=Movie.objects.filter(slug_title=slug_title)
        )
    )
