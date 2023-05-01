from movie import selectors as movie_selectors
from movie.models import Movie
from tests import factories
from tests.base import BaseTest


class MovieSelectorTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        """
        GIVEN:
            - movie1 - watched by user1 and user2
                     - recommend by user1 (vote 7) (watched on NETFLIX)
                     - recommend by user2 (vote 3) (watched on AMAZON_PRIME)
            - movie2 - watched by user2 (vote 3)
            ---------------------------------------
            - user3 - no movie watched

        """
        super().setUpClass()

        # create movies
        cls.movie1 = factories.MovieFactory()
        cls.movie2 = factories.MovieFactory()

        # set watchers
        cls.movie1.watchers.set([cls.user1, cls.user2])
        cls.movie2.watchers.set([cls.user2])

        # set recommendations
        factories.UserRecommendMovieFactory(
            user=cls.user1,
            movie=cls.movie1,
            platform=factories.PlatformFactory(name='NETFLIX'),
            vote=7,
        )
        factories.UserRecommendMovieFactory(
            user=cls.user2,
            movie=cls.movie1,
            platform=factories.PlatformFactory(name='AMAZON_PRIME'),
            vote=3,
        )

        # all movies
        cls.movies = Movie.objects.all()

    def test_movies_user_has_watched(self):
        """
        GIVEN what set up in `setUpClass`
        WHEN selector function `movies_user_has_watched` is called with `has_watched=True`
        THEN
            user1 receives 1 movie (movie1)
            user2 receives 2 movies
            user3 receives 0 movies
        WHEN selector function `movies_user_has_watched` is called with `has_watched=False`
        THEN
            user1 receives 1 movie (movie2)
            user2 receives 0 movies
            user3 receives 2 movies

        """
        movies = Movie.objects.all()
        self.assertEqual(movies.count(), 2)

        # user1
        user1_movies = movie_selectors.movies_user_has_watched(
            movies=movies,
            user=self.user1,
            has_watched=True,
        )
        self.assertEqual(user1_movies.count(), 1)
        self.assertEqual(user1_movies.first().title, self.movie1.title)
        user1_not_movies = movie_selectors.movies_user_has_watched(
            movies=movies,
            user=self.user1,
            has_watched=False,
        )
        self.assertEqual(user1_not_movies.count(), 1)
        self.assertNotEqual(user1_not_movies.first().title, self.movie1.title)

        # user 2
        user2_movies = movie_selectors.movies_user_has_watched(
            movies=movies,
            user=self.user2,
            has_watched=True,
        )
        self.assertEqual(user2_movies.count(), 2)
        user2_not_movies = movie_selectors.movies_user_has_watched(
            movies=movies,
            user=self.user2,
            has_watched=False,
        )
        self.assertEqual(user2_not_movies.count(), 0)

        # user3
        user3_movies = movie_selectors.movies_user_has_watched(
            movies=movies,
            user=self.user3,
            has_watched=True,
        )
        self.assertEqual(user3_movies.count(), 0)
        user3_not_movies = movie_selectors.movies_user_has_watched(
            movies=movies,
            user=self.user3,
            has_watched=False,
        )
        self.assertEqual(user3_not_movies.count(), 2)

    def test_movies_recommend_by_others_by_avg(self):
        """
        GIVEN what set up in `setUpClass`
        WHEN selector function `movies_recommend_by_others_by_avg` is called
        THEN
            user1 receives 0 movies (movie2 has no recommendations)
            user2 receives 0 movies (already watched all movies)
            user3 receives 1 movies (movie1 with average = 5)
        """
        user1_query = movie_selectors.movies_recommend_by_others_by_avg(
            movies=self.movies,
            user=self.user1,
        )
        self.assertEqual(user1_query.count(), 0)

        user2_query = movie_selectors.movies_recommend_by_others_by_avg(
            movies=self.movies,
            user=self.user2,
        )
        self.assertEqual(user2_query.count(), 0)

        user3_query = movie_selectors.movies_recommend_by_others_by_avg(
            movies=self.movies,
            user=self.user3,
        )
        self.assertEqual(user3_query.count(), 1)
        self.assertEqual(user3_query.first().vote_avg, 5)

    def test_movie_get_filtered(self):
        """Test filter class"""

        # Test filter by title
        mock_request = factories.MockRequestFactory(
            query_params={"title": "movie_title0"},
            user=self.user1,
        )
        movies = movie_selectors.movie_get_filtered(
            request=mock_request,
        )
        self.assertEqual(movies.count(), 1)
        self.assertEqual(movies.first().title, 'movie_title0')

        # test sorting by title
        mock_request = factories.MockRequestFactory(
            query_params={"order_by_title": "-title"},
            user=self.user1,
        )
        movies = movie_selectors.movie_get_filtered(
            request=mock_request,
        )
        self.assertEqual(movies.count(), 2)
        self.assertEqual(movies.first().title, 'movie_title1')
