from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from ..models import Cycle

def cyclelist(request):
    cycles = Cycle.objects.all()
    context = {'cycles': cycles}
    print(context)
    return render(request, 'cycles/cyclelist.html', context)