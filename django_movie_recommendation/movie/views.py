from common.permissions import IsAuthenticatedForWriting
from common.serializers import serialize_input_data
from movie import selectors, services
from movie.serializers import InputMovieSerializer, OutputMovieSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class MovieListCreateView(APIView):
    permission_classes = (IsAuthenticatedForWriting,)

    def get(self, request):
        movies = selectors.movie_get(
            request=request,
        )
        data = OutputMovieSerializer(movies, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        # serialize input data
        validated_data = serialize_input_data(
            input_serializer=InputMovieSerializer, data=request.data
        )

        created_movie = services.movie_create(
            **validated_data,
        )

        ser_data = OutputMovieSerializer(created_movie).data
        return Response(ser_data, status=status.HTTP_201_CREATED)


class MovieRetrieveView(APIView):
    def get(self, request, slug_title: str):
        movie = selectors.movie_get_one(
            user=request.user,
            slug_title=slug_title,
        )
        data = OutputMovieSerializer(movie, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)


class MovieSwitchWatched(APIView):
    permission_classes = (IsAuthenticatedForWriting,)

    def post(self, request, slug_title: str):
        movie = services.movie_switch_watched(
            user=request.user,
            slug_title=slug_title,
        )
        data = OutputMovieSerializer(movie, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
