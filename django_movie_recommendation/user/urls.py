from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserListView, UserRegistrationView

user_patterns = [
    path('', UserListView.as_view(), name='user__list'),
    path('register', UserRegistrationView.as_view(), name='user__registration'),
    path('login', TokenObtainPairView.as_view(), name='user__token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='user__token_refresh'),
]

urlpatterns = [
    path('user/', include((user_patterns, 'user'))),
]
