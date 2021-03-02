from django.urls import path

from .views import user_views, auth_views, my_profile_views, group_views


urlpatterns = [
    # profile routes
    path(r'users', user_views.UserListCreateAPIView.as_view()),
    path(r'users/all', user_views.ALLUserListAPIView.as_view()),
    path(r'users/<int:pk>', user_views.UserRetrieveUpdateAPIView.as_view()),
    path(r'users/<int:pk>/activate', user_views.UserActivateAPIView.as_view()),
    path(r'users/<int:pk>/deactivate', user_views.UserDeactivateAPIView.as_view()),

    path(r'myself', my_profile_views.MyProfileRetrieveUpdateAPIView.as_view()),
    path(r'myself/reset-password', my_profile_views.MyProfileUpdatePasswordAPIView.as_view()),

    # Groups/Permissions routes
    path(r'groups', group_views.GroupListCreateAPIView.as_view()),
    path(r'groups/all', group_views.ALLGroupListAPIView.as_view()),
    path(r'groups/<int:pk>', group_views.GroupRetrieveUpdateDestroyAPIView.as_view()),

    path(r'auth/reset-request', auth_views.ForgotPasswordAPIView.as_view()),
    path(r'auth/check-reset-token/<str:token>', auth_views.ForgotPasswordAPIView.as_view()),
    path(r'auth/reset', auth_views.ResetPasswordAPIView.as_view()),
    path(r'auth/register', auth_views.RegisterView.as_view()),
    path(r'auth/login', auth_views.JWTLoginView.as_view())
]
