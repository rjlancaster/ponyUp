from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from datetime import datetime
from ..models import Tenant

def tenantlist(request):
    '''Summary: Captures all of the tenants from the Tenants table and sends it to context

    Arguments:
        request

    Returns:
        Renders the context to the tenantlist template.
    '''
    tenants = Tenant.objects.all()
    context = {'tenants': tenants}
    return render(request, 'cycles/tenantlist.html', context)

def deleteTenant(request, tenant_id):
    '''

    Summary: This function grabs the tenant associated with the tenant_id from the Tenant table.

     After that it submits a deleted on date into the deletedOn field for the tenant.

    Arguments:
     request: Brings back the contents of the template.
     recurring_id: Brings back the id of the current tenant.

    Returns:
     HttpResponseRedirect: Redirects to the tenant list.

    '''
    tenant = Tenant.objects.get(pk=tenant_id)
    todaysDate = datetime.now()
    tenant.deletedOn = todaysDate
    tenant.save()
    return HttpResponseRedirect(reverse('cycles:tenantlist'))

def editTenantForm(request, tenant_id):
    '''Summary: Grabs the tenant name associated with the ID and submits it in context to the form for editing

    Arguments:
        request
        tenant_id

    Returns:
        Renders the context to the edit Tenant Form template.
    '''
    tenantRow = get_object_or_404(Tenant, pk=tenant_id)
    context = {'tenant': tenantRow}
    return render(request, 'cycles/editTenantForm.html', context)

def editTenant(request, tenant_id):
    """This method is executed when the user saves the updated tenant info on the form page]

    Arguments:
        request
        tenant_id

    Returns:
        User is redirected to main tenant list page.
    """
    tenant = Tenant.objects.get(pk=tenant_id)
    tenant.name = request.POST['name']
    tenant.income = request.POST['income']
    tenant.save()
    return HttpResponseRedirect(reverse('cycles:tenantlist'))

def addTenantForm(request):
    return render(request, 'cycles/addTenantForm.html')

def addTenant(request):
    """This method is executed when the user saves the new tenant on the form page]

    Arguments:
        request

    Returns:
        User is redirected to main tenant list page.
    """
    managerId = request.user.id
    name = request.POST['name']
    income = request.POST['income']
    new_tenant = Tenant.objects.create(
        name = name,
        income = income,
        manager = User.objects.get(pk=managerId)
    )
    return HttpResponseRedirect(reverse('cycles:tenantlist'))
