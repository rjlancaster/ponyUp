from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count, Sum
from ..models import Cycle, Tenant, tenantCycle, Bills

def cyclelist(request):
    cycles = Cycle.objects.all()
    context = {'cycles': cycles}
    return render(request, 'cycles/cyclelist.html', context)

def cycleDetail(request, cycle_id):
    managerId = request.user.id
    recurringBills = Bills.objects.filter(recurring=1, cycle=cycle_id)
    recurringBillsDue = Bills.objects.filter(recurring=1, cycle=cycle_id).aggregate(Sum('amount'))
    oneTimeBills = Bills.objects.filter(recurring=0, cycle=cycle_id)
    oneTimeBillsDue = Bills.objects.filter(recurring=0, cycle=cycle_id).aggregate(Sum('amount'))
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    tenants = Tenant.objects.filter(deletedOn=None, pk=managerId)
    currentTenants = Tenant.objects.filter(cycle=cycle_id)
    allBillsDue = Bills.objects.filter(cycle=cycle_id).aggregate(Sum('amount'))
    allBillsDueInt = allBillsDue['amount__sum']
    numberOfTenants = Tenant.objects.filter(cycle=cycle_id).count()
    duePerTenant = allBillsDueInt/numberOfTenants
    context = {'recurringBills' : recurringBills, 'recurringBillsDue': recurringBillsDue, 'allBillsDue': allBillsDue, 'oneTimeBillsDue': oneTimeBillsDue, 'oneTimeBills' : oneTimeBills, 'cycle': cycle, 'tenants': tenants, 'currentTenants': currentTenants, 'duePerTenant': duePerTenant}
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

def editBillForm(request, bill_id):
    billRow = get_object_or_404(Bills, pk=bill_id)
    context = {'billRow': billRow}
    return render(request, 'cycles/editBillForm.html', context)

def editBill(request, bill_id):
    """R Lancaster[This method is executed when the user saves the updated user settings on the user settings update form page]

    Arguments:
        request

    Returns:
        User is redirected to main User Settings page.
    """
    bill = Bills.objects.get(pk=bill_id)
    bill.name = request.POST['name']
    bill.amount = request.POST['amount']
    bill.save()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(bill.cycle.id,)))

def deleteBill(request, bill_id):
    bill = Bills.objects.get(pk=bill_id)
    bill.delete()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(bill.cycle.id,)))

def addRecurringForm(request, cycle_id):
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    context = {'cycle': cycle}
    return render(request, 'cycles/addRecurringForm.html', context)

def addRecurring(request, cycle_id):
    name = request.POST['name']
    amount = request.POST['amount']
    new_tenant = Bills.objects.create(
        name = name,
        amount = amount,
        recurring = 1,
        cycle = Cycle.objects.get(pk=cycle_id)
    )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle_id, )))

def addOneTimeForm(request, cycle_id):
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    context = {'cycle': cycle}
    return render(request, 'cycles/addOneTimeForm.html', context)

def addOneTime(request, cycle_id):
    name = request.POST['name']
    amount = request.POST['amount']
    new_tenant = Bills.objects.create(
        name = name,
        amount = amount,
        recurring = 0,
        cycle = Cycle.objects.get(pk=cycle_id)
    )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle_id, )))

def newCycleForm(request):
    managerId = request.user.id
    print(managerId)
    tenants = Tenant.objects.filter(deletedOn=None, manager_id=managerId)
    print(tenants)
    context = {'tenants': tenants}
    return render(request, 'cycles/newCycleForm.html', context)

def newCycle(request):
    managerId = request.user.id
    name = request.POST['name']
    tenantId = request.POST['tenant']
    endDate = request.POST['date']
    print(tenantId)
    print(endDate)
    billingCycle = Cycle.objects.create(
        name = name,
        endDate = endDate,
        tenant = Tenant.objects.get(pk=name.id)
    )
    # tenantCycle = Tenantcycle.objects.create(
    #     cycle =
    # )

    # return HttpResponseRedirect(reverse('cycles:tenantlist'))
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(billingCycle.id)))
