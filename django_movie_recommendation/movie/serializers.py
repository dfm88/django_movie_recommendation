from common.serializers import BaseMeta
from django.contrib.auth.validators import UnicodeUsernameValidator
from movie.models import Movie, Platform
from rest_framework import serializers

"""PLATFORM"""


class InputPlatformSerializer(serializers.ModelSerializer):
    class Meta(BaseMeta):
        model = Platform
        # ref https://medium.com/django-rest-framework/dealing-with-unique-constraints-in-nested-serializers-dade33b831d9  # noqa
        extra_kwargs = {
            'name': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


class OutputPlatformSerializer(InputPlatformSerializer):
    pass


"""MOVIE"""


class InputMovieSerializer(serializers.ModelSerializer):
    platforms = InputPlatformSerializer(many=True)
    slug_title = serializers.CharField(required=False)

    class Meta(BaseMeta):
        model = Movie
        exclude = ('watchers',)


class OutputMovieSerializer(InputMovieSerializer):
    watched = serializers.BooleanField(required=False)
