import django_filters
from django.db import models
from django.http import HttpRequest
from recommendation.models import UserRecommendMovie


class RecommendationFilter(django_filters.FilterSet):
    # filter by platform name
    platform = django_filters.CharFilter(field_name='platform', lookup_expr='name')
    # filter by user to get all recommendation of the given user
    user = django_filters.CharFilter(field_name='user', lookup_expr='username')
    # filter to allow sorting by platform name
    platform__name = django_filters.CharFilter(
        field_name='platform', lookup_expr='name'
    )
    # sorting filter by vote or platform name
    order_by = django_filters.OrderingFilter(
        fields=(
            ('vote', 'vote'),
            ('platform__name', 'platform'),
        ),
    )

    class Meta:
        model = UserRecommendMovie
        fields = [
            'user',
            'platform',
        ]


def recommendation_get(
    request: HttpRequest,
) -> models.QuerySet[UserRecommendMovie]:
    query = UserRecommendMovie.objects.select_related(
        'user',
        'movie',
        'platform',
    ).all()
    mf = RecommendationFilter(
        data=request.GET,
        queryset=query,
        request=request,
    )
    return mf.qs


def recommendation_on_movie_get(
    request: HttpRequest,
    slug_title: str,
) -> models.QuerySet[UserRecommendMovie]:
    """Return the list of recommendations for the given movie
    filtered by request params

    Args:
        request (HttpRequest)
        slug_title (str)

    Returns:
        models.QuerySet[UserRecommendMovie]
    """
    qs = recommendation_get(request=request)
    qs = qs.filter(movie__slug_title=slug_title)
    return qs


def recommendation_on_user_get(
    request: HttpRequest,
    username: str,
) -> models.QuerySet[UserRecommendMovie]:
    """Return the list of recommendations for the given username
    filtered by request params

    Args:
        request (HttpRequest)
        username (str)

    Returns:
        models.QuerySet[UserRecommendMovie]
    """
    qs = recommendation_get(request=request)
    qs = qs.filter(user__username=username)
    return qs
