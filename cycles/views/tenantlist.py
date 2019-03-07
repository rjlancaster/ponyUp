from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from datetime import datetime
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
    tenant = Tenant.objects.get(pk=tenant_id)
    todaysDate = datetime.now()
    tenant.deletedOn = todaysDate
    tenant.save()
    return HttpResponseRedirect(reverse('cycles:tenantlist'))

def editTenantForm(request, tenant_id):
    tenantRow = get_object_or_404(Tenant, pk=tenant_id)
    context = {'tenant': tenantRow}
    return render(request, 'cycles/editTenantForm.html', context)

def editTenant(request, tenant_id):
    """R Lancaster[This method is executed when the user saves the updated user settings on the user settings update form page]

    Arguments:
        request

    Returns:
        User is redirected to main User Settings page.
    """
    tenant = Tenant.objects.get(pk=tenant_id)
    tenant.name = request.POST['name']
    tenant.income = request.POST['income']
    # print(tenant.name, tenant.income)
    tenant.save()
    return HttpResponseRedirect(reverse('cycles:tenantlist'))

def addTenantForm(request):
    return render(request, 'cycles/addTenantForm.html')

def addTenant(request):
    """R Lancaster[This method is executed when the user saves the updated user settings on the user settings update form page]

    Arguments:
        request

    Returns:
        User is redirected to main User Settings page.
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