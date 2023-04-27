from common.serializers import serialize_input_data
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user import services
from user.models import UserCustom
from user.serializers import InputUserSerializer, OutputUserSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        # serialize input data
        validated_data = serialize_input_data(
            input_serializer=InputUserSerializer,
            data=request.data,
        )
        created_user = services.user_registration(
            **validated_data,
        )
        data = OutputUserSerializer(created_user).data
        return Response(data=data, status=status.HTTP_201_CREATED)


class UserListView(APIView):
    def get(self, request):
        users = UserCustom.objects.all()
        data = OutputUserSerializer(users, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
