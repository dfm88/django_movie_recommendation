from django.urls import include, path
from recommendation.views import (
    RecommendationMovieListCreateView,
    RecommendationUserListView,
)

recommendation_patterns = [
    path(
        'movie/<str:slug_title>',
        RecommendationMovieListCreateView.as_view(),
        name='recommendation_movie__list_create',
    ),
    path(
        'user/<str:username>',
        RecommendationUserListView.as_view(),
        name='recommendation_user__list',
    ),
]

urlpatterns = [
    path('', include((recommendation_patterns, 'recommendation'))),
]
