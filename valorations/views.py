from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages 

from drivers.models import Driver
from .models import Valoration

login_required()
permission_required('valorations.add_valoration')
def create_valoration_view(request, slug):
    template_name = 'valorations/create.html'
    title = 'Calificar motorizado'
    driver = Driver.objects.get(slug=slug)
    client = request.user.client if request.user.is_client else None
    if request.method == 'POST':
        rating = request.POST.get('rating')
        experience = request.POST.get('experience')
        Valoration.objects.create(
            driver=driver,
            client=client,
            rating=int(rating),
            experience=experience
        )
        messages.success(request, 'Calificación realizada con éxito')
        return redirect('drivers:detail', slug=driver.slug)

    return render(request, template_name, context={
        'title': title
    })

login_required()
permission_required('valorations.change_valoration')
def create_valoration_view(request, slug, pk):
    template_name = 'valorations/edit.html'
    title = 'Editar calificación del motorizado'
    driver = Driver.objects.get(slug=slug)
    client = request.user.client if request.user.is_client else None
    if request.method == 'POST':
        rating = request.POST.get('rating')
        experience = request.POST.get('experience')
        Valoration.objects.create(
            driver=driver,
            client=client,
            rating=int(rating),
            experience=experience
        )
        messages.success(request, 'Calificación realizada con éxito')
        return redirect('drivers:detail', slug=driver.slug)

    return render(request, template_name, context={
        'title': title
    })