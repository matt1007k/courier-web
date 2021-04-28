from django.urls import path

from .views import DeleteDetailView

app_name = 'details'

urlpatterns = [
    path('<int:pk>/delete/', DeleteDetailView.as_view(), name="delete")
]