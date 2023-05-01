from typing import Iterable, Iterator

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.shortcuts import get_object_or_404
from movie import selectors
from movie.models import Movie, MovieGenreChoice, Platform
from user.models import UserCustom


def platforms_get_or_create(
    platforms: list[dict],
) -> Iterator[Platform]:
    for platform in platforms:
        db_platform, _ = Platform.objects.get_or_create(name=platform['name'])
        yield db_platform


def set_platforms_to_movie(
    platforms: Iterable[Platform],
    movie: Movie,
) -> Movie:
    movie.platforms.set(platforms)
    return movie


def add_platform_to_movie(
    platform: Platform,
    movie: Movie,
) -> Movie:
    movie.platforms.add(platform)
    return movie


@transaction.atomic
def movie_create(
    platforms: list[dict],
    title: str,
    genre: MovieGenreChoice,
) -> Movie:
    """Create movie and associate it to platforms

    Args:
        platforms (list[dict])
        title (str)
        genre (MovieGenreChoice)

    Returns:
        Movie
    """
    movie = Movie.objects.create(title=title, genre=genre)
    platforms_db = platforms_get_or_create(
        platforms=platforms,
    )
    movie = set_platforms_to_movie(
        platforms=platforms_db,
        movie=movie,
    )

    movie.full_clean()
    movie.save()
    return movie


def movie_switch_watched(
    user: UserCustom | AnonymousUser,
    slug_title: str,
) -> Movie:
    """Set/unset a movie as 'watched' for user

    Args:
        user (UserCustom | AnonymousUser)
        slug_title (str)

    Returns:
        Movie
    """
    movie = get_object_or_404(Movie, slug_title=slug_title)

    user_watched_movie = movie.watchers.filter(username=user.username).exists()

    if user_watched_movie:
        movie.watchers.remove(user)
    else:
        movie.watchers.add(user)

    # to set "watched" attr
    movie = selectors.movie_get_one(
        user=user,
        slug_title=slug_title,
    )
    return movie
