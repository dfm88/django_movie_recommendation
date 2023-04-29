from django.db import IntegrityError
from movie import selectors as movie_selectors
from movie.services import add_platform_to_movie, platforms_get_or_create
from recommendation.models import UserRecommendMovie
from user.models import UserCustom


def recommendation_movie_create(
    user: UserCustom,
    slug_title: str,
    vote: int,
    comment: str,
    platform: dict,
) -> UserRecommendMovie:
    """Insert a new recommendation from user
    for the given movie title. It also takes the platform
    on which the user watched the movie

    Args:
        user (UserCustom)
        slug_title (str)
        vote (int)
        comment (str)
        platform (dict)

    Raises:
        IntegrityError: If user already recommend the movie

    Returns:
        UserRecommendMovie
    """

    movie = movie_selectors.movie_get_one(
        user=user,
        slug_title=slug_title,
    )

    platform_db = next(platforms_get_or_create(platforms=[platform]))

    movie = add_platform_to_movie(
        platform=platform_db,
        movie=movie,
    )

    try:
        recommendation = UserRecommendMovie.objects.create(
            user=user,
            movie=movie,
            vote=vote,
            comment=comment,
            platform=platform_db,
        )
    except IntegrityError as ie:
        raise IntegrityError("User already recommend this movie") from ie

    recommendation.full_clean()
    recommendation.save()
    return recommendation
