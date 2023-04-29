from common.serializers import BaseMeta
from django.contrib.auth.validators import UnicodeUsernameValidator

# from recommendation.serializers import OutputRecommendationSerializerLight
from movie.models import Movie, Platform
from rest_framework import serializers

"""PLATFORM"""


class PlatformBaseSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = Platform
        # ref https://medium.com/django-rest-framework/dealing-with-unique-constraints-in-nested-serializers-dade33b831d9  # noqa
        extra_kwargs = {
            'name': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


"""MOVIES"""


class MovieBaseSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = Movie
        exclude = (
            *BaseMeta.exclude,
            'watchers',
        )


class MovieBaseSerializerLight(MovieBaseSerializer):
    class Meta(BaseMeta):
        model = Movie
        exclude = (
            *BaseMeta.exclude,
            "watchers",
            "platforms",
            "recommenders",
        )
