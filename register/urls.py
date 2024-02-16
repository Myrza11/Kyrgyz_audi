from django.urls import path
from register.views import *
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', CustomUserLoginView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('change-username/', ChangeUsernameView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('user-list/', UserListView.as_view()),
    path('user-update/<int:pk>/', UserUpdateView.as_view()),
    path('user-profile/', UserProfileView.as_view()),
    path('check-username/', CheckUsernameView.as_view()),

]