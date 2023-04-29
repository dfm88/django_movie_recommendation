from common.serializers import BaseMeta
from movie.serializers.serializers_base import (
    MovieBaseSerializer,
    PlatformBaseSerializer,
)
from recommendation.models import UserRecommendMovie
from recommendation.serializers.serializers_base import (
    RecommendationBaseSerializer,
    RecommendationBaseSerializerWithUser,
)


class InputRecommendationSerializer(RecommendationBaseSerializer):
    platform = PlatformBaseSerializer()

    class Meta(BaseMeta):
        model = UserRecommendMovie
        exclude = (
            *BaseMeta.exclude,
            'movie',
            'user',
        )


class OutputRecommendationSerializer(RecommendationBaseSerializerWithUser):
    platform = PlatformBaseSerializer()

    class Meta(BaseMeta):
        model = UserRecommendMovie


class OutputRecommendationSerializerWithMovie(OutputRecommendationSerializer):
    movie = MovieBaseSerializer()
