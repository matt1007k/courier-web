from django.urls import path

from .views import DeleteDetailView, origin_map_view, destiny_map_view

app_name = 'details'

urlpatterns = [
    path('<int:pk>/delete/', DeleteDetailView.as_view(), name="delete"),
    path('<int:pk>/origin-map/', origin_map_view, name="origin-map"),
    path('<int:pk>/destiny-map/', destiny_map_view, name="destiny-map")
]