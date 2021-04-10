from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def dashboard(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'admin/dashboard.html', context=context)


def custom_page_not_found_view(request, exception):
    context = {}
    return render(request, "errors/404.html", context=context)
