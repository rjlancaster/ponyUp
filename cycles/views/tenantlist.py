from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from ..models import Tenant

def tenantlist(request):
    tenants = Tenant.objects.all()
    context = {'tenants': tenants}
    return render(request, 'cycles/tenantlist.html', context)

def deleteTenant(request, tenant_id):
    '''

    Summary: This function grabs the tenant_id from the template.
     Then it seeks and selects the tenant row whose product key matches the tenant_id
     and sticks it into the tenant variable.

     After that it deletes that tenant.

    Arguments:
     request: Brings back the contents of the template.
     tenant_id: Brings back the id of the current tenant.

    Returns:
     HttpResponseRedirect: Redirects to the tenant list.

    '''
    tenants = get_object_or_404(Tenant, pk=tenant_id)
    tenant_id = tenant.id
    tenant = Tenant.objects.filter(pk=tenant_id)
    tenant.delete()
    return HttpResponseRedirect(reverse('cycles:tenants'))