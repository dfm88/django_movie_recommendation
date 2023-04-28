from typing import Iterator

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from movie import selectors
from movie.models import Movie, MovieGenreChoice, Platform
from user.models import UserCustom


def platforms_get_or_create(
    platforms: list[dict],
) -> Iterator[Platform]:
    for platform in platforms:
        db_platform, _ = Platform.objects.get_or_create(name=platform['name'])
        yield db_platform


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

    db_platforms = platforms_get_or_create(platforms=platforms)
    movie.platforms.set(db_platforms)

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
    movie = selectors.movie_get_one(
        user=user,
        slug_title=slug_title,
    )

    if movie.watchers.filter(username=user.username).exists():
        movie.watchers.remove(user)
    else:
        movie.watchers.add(user)

    return movie
