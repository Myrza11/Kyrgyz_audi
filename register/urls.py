from django.urls import path
from register.views import *
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', CustomUserLoginView.as_view()),
    path('refresh-token/', CustomUserTokenRefreshView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('change-username/', ChangeUsernameView.as_view()),
    path('logout/', TokenBlacklistView.as_view(), name='token_logout'),
    path('user-list/', UserListView.as_view()),
    path('user-update/<int:pk>/', UserUpdateView.as_view()),
]