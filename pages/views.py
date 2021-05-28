from django.shortcuts import render

def index_view(request):
    return render(request, 'pages/home.html', context={})

def error_404(request, exception):
        data = {}
        return render(request,'errors/404.html', data)

def error_403(request, exception):
        data = {}
        return render(request,'errors/403.html', data)

def error_500(request, exception=None):
        data = {}
        return render(request,'errors/500.html', data)
        