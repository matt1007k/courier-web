from django.urls import path

from .views import DeleteDetailView

app_name = 'details'

urlpatterns = [
    path('delete/<int:pk>/', DeleteDetailView.as_view(), name="delete")
]