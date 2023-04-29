from common.permissions import IsAuthenticatedForWriting
from common.serializers import serialize_input_data
from recommendation import selectors, services
from recommendation.serializers.serializers import (
    InputRecommendationSerializer,
    OutputRecommendationSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RecommendationMovieListCreateView(APIView):
    permission_classes = (IsAuthenticatedForWriting,)

    def get(self, request, slug_title: str):
        recommendations = selectors.recommendation_on_movie_get(
            request=request,
            slug_title=slug_title,
        )
        data = OutputRecommendationSerializer(recommendations, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, slug_title: str):
        # serialize input data
        validated_data = serialize_input_data(
            input_serializer=InputRecommendationSerializer, data=request.data
        )

        created_movie = services.recommendation_movie_create(
            user=request.user,
            slug_title=slug_title,
            **validated_data,
        )

        ser_data = OutputRecommendationSerializer(created_movie).data
        return Response(ser_data, status=status.HTTP_201_CREATED)


class RecommendationUserListView(APIView):
    permission_classes = (IsAuthenticatedForWriting,)

    def get(self, request, username: str):
        recommendations = selectors.recommendation_on_user_get(
            request=request,
            username=username,
        )
        data = OutputRecommendationSerializer(recommendations, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
