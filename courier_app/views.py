from django.shortcuts import render

def dashboard(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'admin/dashboard.html', context=context)