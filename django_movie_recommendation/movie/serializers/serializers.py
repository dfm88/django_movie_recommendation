from common.serializers import BaseMeta
from movie.models import Movie
from movie.serializers.serializers_base import (
    MovieBaseSerializer,
    PlatformBaseSerializer,
)
from recommendation.serializers.serializers_base import (
    RecommendationBaseSerializerWithUser,
)
from rest_framework import serializers

"""PLATFORM"""


class InputPlatformSerializer(PlatformBaseSerializer):
    pass


class OutputPlatformSerializer(PlatformBaseSerializer):
    pass


"""MOVIE"""


class InputMovieSerializer(MovieBaseSerializer):
    platforms = PlatformBaseSerializer(many=True)
    slug_title = serializers.CharField(required=False)


class OutputMovieSerializer(InputMovieSerializer):
    watched = serializers.BooleanField(required=False)
    recommendations = RecommendationBaseSerializerWithUser(
        many=True, read_only=True, source='userrecommendmovie_set'
    )

    class Meta(BaseMeta):
        model = Movie
        exclude = (
            *InputMovieSerializer.Meta.exclude,
            "recommenders",
        )
