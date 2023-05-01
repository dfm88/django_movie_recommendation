import factory
from django.contrib.auth.models import AnonymousUser, User
from django.utils.text import slugify
from factory import fuzzy
from movie.models import (
    Movie,
    MovieGenreChoice,
    MoviePlatformChoice,
    Platform,
    UserWatchedMovie,
)
from recommendation.models import UserRecommendMovie
from user.models import UserCustom

"""REQUEST"""


class MockRequestFactory:
    def __init__(self, query_params: dict, user: AnonymousUser | User):
        self.query_params = query_params
        self.user = user

    @property
    def GET(self) -> dict:
        return self.query_params


"""USER"""


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserCustom
        django_get_or_create = ('username', 'email')

    username = factory.Sequence(lambda n: f"test_user{n+1}")
    password = factory.PostGenerationMethodCall('set_password', 'test')
    email = factory.LazyAttributeSequence(
        lambda o, n: '%s@s%d.mail.com' % (o.username, n)
    )


"""PLATFORM"""


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Platform
        django_get_or_create = ('name',)

    name = fuzzy.FuzzyChoice(MoviePlatformChoice)


"""MOVIE"""


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie
        django_get_or_create = ('title', 'slug_title')

    title = factory.Sequence(lambda n: f"movie_title{n}")
    slug_title = factory.LazyAttribute(lambda o: slugify(o.title))
    genre = fuzzy.FuzzyChoice(MovieGenreChoice)

    @factory.post_generation
    def platforms(self, create, extracted, **kwargs):
        # if factory is not created, do nothing
        if not create:
            return
        # if no platform is passed create two fixed platforms
        else:
            # Simple build, do nothing.
            self.platforms.set(
                [
                    PlatformFactory(name=MoviePlatformChoice.AMAZON_PRIME),
                    PlatformFactory(name=MoviePlatformChoice.NETFLIX),
                ]
            )
        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.platforms.add(group)


"""USER WATCHED MOVIE (Through)"""


class UserWatchedMovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserWatchedMovie

    user = factory.SubFactory(UserFactory)
    movie = factory.SubFactory(MovieFactory)


class MovieWatchedBy1UserFactory(MovieFactory):
    membership = factory.RelatedFactory(
        UserWatchedMovieFactory,
        factory_related_name='movie',
    )


"""USER RECOMMEND MOVIE (Through)"""


class UserRecommendMovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRecommendMovie

    user = factory.SubFactory(UserFactory)
    movie = factory.SubFactory(MovieFactory)
    platform = factory.SubFactory(PlatformFactory)
    vote = 1
    comment = ""


class MovieRecommenddBy1UserFactory(MovieFactory):
    membership = factory.RelatedFactory(
        UserRecommendMovieFactory,
        factory_related_name='movie',
    )
