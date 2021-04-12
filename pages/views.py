from django.shortcuts import render

def index_view(request):
    return render(request, 'pages/index.html', context={})

def error_404(request, exception):
        data = {}
        return render(request,'pages/404.html', data)