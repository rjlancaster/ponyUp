from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from ..models import Cycle, Tenant, tenantCycle, Bills

def cyclelist(request):
    cycles = Cycle.objects.all()
    context = {'cycles': cycles}
    return render(request, 'cycles/cyclelist.html', context)

def cycleDetail(request, cycle_id):
    managerId = request.user.id
    recurringBills = Bills.objects.filter(recurring=1, cycle=cycle_id)
    recurringBillsDue = Bills.objects.filter(recurring=1, cycle=cycle_id).count()
    # print(recurringBillsDue)
    oneTimeBills = Bills.objects.filter(recurring=0, cycle=cycle_id)
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    tenants = Tenant.objects.filter(deletedOn=None, pk=managerId)
    currentTenants = Tenant.objects.filter(cycle=cycle_id)
    numberOfTenants = Tenant.objects.filter(cycle=cycle_id).count()
    print(numberOfTenants)
    context = {'recurringBills' : recurringBills, 'recurringBillsDue': recurringBillsDue, 'oneTimeBills' : oneTimeBills, 'cycle': cycle, 'tenants': tenants, 'currentTenants': currentTenants}
    return render(request, 'cycles/cycleDetail.html', context)

def deleteCycle(request, cycle_id):
    '''
    Summary: This function grabs the cycle_id from the template.
     Then it seeks and selects the Cycle row whose product key matches the cycle_id
     and sticks it into the cycle variable.

     After that it deletes that cycle.

    Arguments:
     request: Brings back the contents of the template.
     cycle_id: Brings back the id of the current cycle.

    Returns:
     HttpResponseRedirect: Redirects to the index of this program.
    '''
    cycles = get_object_or_404(Cycle, pk=cycle_id)
    cycle_id = cycles.id
    cycle = Cycle.objects.filter(pk=cycle_id)
    cycle.delete()
    return HttpResponseRedirect(reverse('cycles:index'))
