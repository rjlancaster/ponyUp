from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count, Sum
from ..models import Cycle, Tenant, tenantCycle, Bills, Recurring
from cycles.forms import CycleForm, TenantForm
from django.db import connection


def cyclelist(request):
    cycles = Cycle.objects.all().order_by('-endDate')
    context = {'cycles': cycles}
    return render(request, 'cycles/cyclelist.html', context)


def cycleDetail(request, cycle_id):
    managerId = request.user.id
    recurringBills = Bills.objects.filter(recurring=1, cycle=cycle_id)
    recurringBillsDue = Bills.objects.filter(
        recurring=1, cycle=cycle_id).aggregate(Sum('amount'))
    oneTimeBills = Bills.objects.filter(recurring=0, cycle=cycle_id)
    oneTimeBillsDue = Bills.objects.filter(
        recurring=0, cycle=cycle_id).aggregate(Sum('amount'))
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    allBillsDue = Bills.objects.filter(cycle=cycle_id).aggregate(Sum('amount'))
    allBillsDueInt = allBillsDue['amount__sum']
    tenants = Tenant.objects.filter(deletedOn=None, pk=managerId)
    currentTenants = Tenant.objects.filter(cycle=cycle_id)
    currentTenantsIncome = Tenant.objects.filter(
        cycle=cycle_id).aggregate(Sum('income'))
    currentTenantsIncomeInt = currentTenantsIncome['income__sum']
    percentAmtDueSplit = dict()
    duePerTenant = list()
    numberOfTenants = Tenant.objects.filter(cycle=cycle_id).count()
    if allBillsDueInt == None:
        allBillsDueInt = 0

    if cycle.split == 0:
        for tenant in currentTenants:
            if numberOfTenants == 1:
                duePerTenant = allBillsDueInt
            else:
                duePerTenant = allBillsDueInt/numberOfTenants

    elif cycle.split == 1:
        for tenant in currentTenants:
            tenantName = tenant.name
            incomePercent = tenant.income/currentTenantsIncomeInt
            percentAmtDue = allBillsDueInt*incomePercent
            percentAmtDueSplit[tenantName] = percentAmtDue

    context = {'recurringBills': recurringBills, 'recurringBillsDue': recurringBillsDue, 'allBillsDue': allBillsDue, 'oneTimeBillsDue': oneTimeBillsDue,
               'oneTimeBills': oneTimeBills, 'cycle': cycle, 'tenants': tenants, 'currentTenants': currentTenants, 'duePerTenant': duePerTenant, 'percentAmtDue': percentAmtDueSplit}
    return render(request, 'cycles/cycleDetail.html', context)


def cycleLock(request, cycle_id):
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    if cycle.inactive == 0:
        cycle.inactive = 1
        cycle.save()
    elif cycle.inactive == 1:
        cycle.inactive = 0
        cycle.save()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle.id,)))

def percentSplit(request, cycle_id):
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    if cycle.split == 0:
        cycle.split = 1
        cycle.save()
    elif cycle.split == 1:
        cycle.split = 0
        cycle.save()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle.id,)))


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
    return HttpResponseRedirect(reverse('cycles:cyclelist'))


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


def addRecurringFormDetail(request, cycle_id):
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    context = {'cycle': cycle}
    return render(request, 'cycles/addRecurringFormDetail.html', context)


def addRecurringDetail(request, cycle_id):
    name = request.POST['name']
    amount = request.POST['amount']
    new_tenant = Bills.objects.create(
        name=name,
        amount=amount,
        recurring=1,
        cycle=Cycle.objects.get(pk=cycle_id)
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
        name=name,
        amount=amount,
        recurring=0,
        cycle=Cycle.objects.get(pk=cycle_id)
    )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle_id, )))


def newCycleForm(request):
    cycle_form = CycleForm()
    # tenant_form = TenantForm()
    managerId = request.user.id
    tenants = Tenant.objects.filter(deletedOn=None, manager_id=managerId)
    context = {'cycle_form': cycle_form.as_p(), 'tenants': tenants}
    return render(request, 'cycles/newCycleForm.html', context)


def newCycle(request):
    name = request.POST['name']
    inactive = 0
    year = request.POST['endDate_year']
    month = request.POST['endDate_month']
    day = request.POST['endDate_day']
    endDate = year + "-" + month + "-" + day
    split = 0
    with connection.cursor() as cursor:
        # raw SQL - Variable names reference the database table columns
        cursor.execute("INSERT into cycles_cycle VALUES(%s, %s, %s, %s, %s)", [
                       None, name, inactive, endDate, split])
    newCycleId = cursor.lastrowid
    newCycle = Cycle.objects.get(pk=newCycleId)
    tenantId = request.POST.getlist('tenant[]')
    for tenants in tenantId:
        tenant = Tenant.objects.get(pk=tenants)
        newTenantCycle = tenantCycle.objects.create(
            cycle=newCycle,
            tenant=tenant
        )
    repeatBills = Recurring.objects.all()
    print(repeatBills)
    for bill in repeatBills:
        newBillCycle = Bills.objects.create(
            name=bill.name,
            amount=0.00,
            recurring=1,
            cycle=newCycle
        )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(newCycleId, )))
