from common.serializers import BaseMeta
from recommendation.models import UserRecommendMovie
from rest_framework import serializers
from user.serializers.serializers import OutputUserSerializerLight


class RecommendationBaseSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = UserRecommendMovie
        exclude = (
            *BaseMeta.exclude,
            'movie',
            'platform',
        )


class RecommendationBaseSerializerWithUser(RecommendationBaseSerializer):
    user = OutputUserSerializerLight()
