from django.urls import include, path
from movie.views import MovieListCreateView, MovieRetrieveView, MovieSwitchWatched

movie_patterns = [
    path('', MovieListCreateView.as_view(), name='movie__list'),
    path('<str:slug_title>', MovieRetrieveView.as_view(), name='movie__detail'),
    path(
        'switch_watched/<str:slug_title>',
        MovieSwitchWatched.as_view(),
        name='movie__set_watched',
    ),
]

urlpatterns = [
    path('', include((movie_patterns, 'movie'))),
]
