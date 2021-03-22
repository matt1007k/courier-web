from django.urls import path
from .views import CompleteInfoClientView, login_view, logout_view, register_view, UserCreateView

app_name = 'auth'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/complete-info/', CompleteInfoClientView.as_view(), name='complete-info'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', UserCreateView.as_view(), name='create')
]