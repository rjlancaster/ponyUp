from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from ..models import Tenant

def tenantlist(request):
    tenants = Tenant.objects.all()
    context = {'tenants': tenants}
    return render(request, 'cycles/tenantlist.html', context)