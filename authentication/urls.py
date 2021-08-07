from django.urls import path

from .views import AvatarUploadView, CompleteInfoClientView, PermissionAuthListApiView, activate_user, change_password_view, edit_profile_view, login_view, logout_view, register_view, CompleteAddressClientView, user_create_client_view, user_create_view

app_name = 'auth'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/complete-info/', CompleteInfoClientView.as_view(), name='complete-info'),
    path('register/complete-address/', CompleteAddressClientView.as_view(), name='complete-address'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change-password'),
    path('avatar-upload/<username>/', AvatarUploadView.as_view(), name='avatar-upload'),
    # path('create/', UserCreateView.as_view(), name='create')
    path('edit-profile/', edit_profile_view, name='edit-profile'),
    path('create/', user_create_view, name='create'),
    path('create-client/', user_create_client_view, name='create-client'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate'),
    path('api/permissions-auth/', PermissionAuthListApiView.as_view()),

]