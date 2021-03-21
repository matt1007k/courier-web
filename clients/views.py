from typing import Any, Dict
from django.views.generic import ListView
from .models import Client

class ClientListVew(ListView):
    template_name = "clients/index.html"
    queryset = Client.objects.all().order_by("-id")
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context