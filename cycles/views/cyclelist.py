from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from ..models import Cycle, Tenant, tenantCycle, Bills, Recurring
from cycles.forms import CycleForm, TenantForm
from django.db import connection


def cyclelist(request):
    '''Summary: Captures all of the cycles from the Cycles table and sends it to context

    Arguments:
        request

    Returns:
        Renders the context to the cyclelist template.
    '''
    managerId = request.user.id
    cycles = Cycle.objects.filter(manager=managerId).order_by('-endDate')
    context = {'cycles': cycles}
    return render(request, 'cycles/cyclelist.html', context)


def cycleDetail(request, cycle_id):
    '''Summary: This method is used when the user views the detail on an existing cycle. Sends context from multiple tables over to the Cycle Detail template view including Bills, Tenant and Cycle. Includes calculations for splitting bills by average or weighted average by household income contribution.

    Arguments:
        request
        cycle_id

    Returns:
        The return sends contexts for multiple values over to the cycle detail template view.
    '''
    # lets the app know the user currently logged in
    managerId = request.user.id
    # selects all recurring bills by cycle and calculates a total
    recurringBills = Bills.objects.filter(recurring=1, cycle=cycle_id)
    recurringBillsDue = Bills.objects.filter(
        recurring=1, cycle=cycle_id).aggregate(Sum('amount'))
    # selects all one-time bills by cycle and calculates a total
    oneTimeBills = Bills.objects.filter(recurring=0, cycle=cycle_id)
    oneTimeBillsDue = Bills.objects.filter(
        recurring=0, cycle=cycle_id).aggregate(Sum('amount'))
    # selects the cycle that the user has selected
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    # calculates all bills for the cycle and transforms into an integer. Needs to be transformed to an integer in order for more calclulations to be run against it.
    allBillsDue = Bills.objects.filter(cycle=cycle_id).aggregate(Sum('amount'))
    allBillsDueInt = allBillsDue['amount__sum']
    # Retrieves tenants for selected cycle (regardless if the tenant ha been "deleted")
    currentTenants = Tenant.objects.filter(cycle=cycle_id)
    # Retrives the total tenant income for tenants in the selected cycle from the Tenant table and transforms to integer
    currentTenantsIncome = Tenant.objects.filter(
        cycle=cycle_id).aggregate(Sum('income'))
    currentTenantsIncomeInt = currentTenantsIncome['income__sum']
    # creates dictionary for use below
    percentAmtDueSplit = dict()
    # creates list for use below
    duePerTenant = list()
    # Counts the the total number of tenants for the selected cycle. Used for average due calc
    numberOfTenants = Tenant.objects.filter(cycle=cycle_id).count()
    # Need this in order to avoid crash. If app tries to divide the number of tenants by a null, system crashes
    if allBillsDueInt == None:
        allBillsDueInt = 0
    # The following logic is used for "average" bill split
    if cycle.split == 0:
        for tenant in currentTenants:
            if numberOfTenants == 1:
                duePerTenant = allBillsDueInt
            else:
                duePerTenant = allBillsDueInt/numberOfTenants
    # The following logic is used for "weighted" average by household income
    elif cycle.split == 1:
        for tenant in currentTenants:
            tenantName = tenant.name
            incomePercent = tenant.income/currentTenantsIncomeInt
            percentAmtDue = allBillsDueInt*incomePercent
            percentAmtDueSplit[tenantName] = percentAmtDue

    context = {'recurringBills': recurringBills, 'recurringBillsDue': recurringBillsDue, 'allBillsDue': allBillsDue, 'oneTimeBillsDue': oneTimeBillsDue,
               'oneTimeBills': oneTimeBills, 'cycle': cycle, 'currentTenants': currentTenants, 'duePerTenant': duePerTenant, 'percentAmtDue': percentAmtDueSplit}
    return render(request, 'cycles/cycleDetail.html', context)


def newCycleForm(request):
    '''Summary: Sends the Cycle Form (for cycle name and end Date) and all tenants belong to the logged in user who are not deleted over to the New Cycle Form as context

    Arguments:
        request

    Returns:
        Return sends info detailed above over as context
    '''

    cycle_form = CycleForm()
    managerId = request.user.id
    tenants = Tenant.objects.filter(deletedOn=None, manager_id=managerId)
    context = {'cycle_form': cycle_form.as_p(), 'tenants': tenants}
    return render(request, 'cycles/newCycleForm.html', context)


def newCycle(request):
    '''Summary: This method retrieves the input sent over from the New Cycle Form and inputs into the appropriate tables in order for the new cycle to be created.

    Arguments:
        request

    Returns:
        Redirects to the Cycle detail page of the cycle that has just been created
    '''
    managerId = request.user.id
    # Retrieving info input from New Cycle Form
    name = request.POST['name']
    year = request.POST['endDate_year']
    month = request.POST['endDate_month']
    day = request.POST['endDate_day']
    # Formatting the date field in a way that SQL needs it to be stored
    endDate = year + "-" + month + "-" + day
    # setting the new cycle as Active and to split bills by average tenants
    inactive = 0
    split = 0
    # SQL insert into Cycle table
    with connection.cursor() as cursor:
        # raw SQL - Variable names reference the database table columns
        cursor.execute("INSERT into cycles_cycle VALUES(%s, %s, %s, %s, %s, %s)", [
                       None, name, inactive, endDate, split, managerId])
    # Retrieves ID from Cycle just created
    newCycleId = cursor.lastrowid
    # Retrieves information about cycle just created
    newCycle = Cycle.objects.get(pk=newCycleId)
    # Logic below required in order to add information to tenantCycle join table so that tenants are assigned to the cycle just created
    tenantId = request.POST.getlist('tenant[]')
    for tenants in tenantId:
        tenant = Tenant.objects.get(pk=tenants)
        newTenantCycle = tenantCycle.objects.create(
            cycle=newCycle,
            tenant=tenant
        )
    # Logic below required in order for recurring bills to be assigned to the new cycle. Recurring bill category will be assigned with dollar amount of zero.
    repeatBills = Recurring.objects.filter(deletedOn=None, manager=managerId)
    for bill in repeatBills:
        newBillCycle = Bills.objects.create(
            name=bill.name,
            amount=0.00,
            recurring=1,
            cycle=newCycle,
            manager = User.objects.get(pk=managerId)
        )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(newCycleId, )))


def cycleLock(request, cycle_id):
    '''Summary: This method controls hiding and unhiding the edit and delete buttons for the selected Cycle

    Arguments:
        request
        cycle_id

    Returns:
        Returns the selected cycle with new values
    '''

    cycle = get_object_or_404(Cycle, pk=cycle_id)
    if cycle.inactive == 0:
        cycle.inactive = 1
        cycle.save()
    elif cycle.inactive == 1:
        cycle.inactive = 0
        cycle.save()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle.id,)))

def percentSplit(request, cycle_id):
    '''Summary: This method controls how the user will see the cycle's household bills divided. User can select to divide bills by average or by weighted average of household income

    Arguments:
        request
        cycle_id

    Returns:
        Returns the selected cycle with new values
    '''

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
     HttpResponseRedirect: Redirects to the list of cycles.
    '''
    cycles = get_object_or_404(Cycle, pk=cycle_id)
    cycle_id = cycles.id
    cycle = Cycle.objects.filter(pk=cycle_id)
    cycle.delete()
    return HttpResponseRedirect(reverse('cycles:cyclelist'))


def editBillForm(request, bill_id):
    '''Summary: Grabs the bill name associated with the ID and submits it in context to the form for editing

    Arguments:
        request
        bill_id

    Returns:
        Renders the context to the edit Bill Form template.
    '''
    billRow = get_object_or_404(Bills, pk=bill_id)
    context = {'billRow': billRow}
    return render(request, 'cycles/editBillForm.html', context)


def editBill(request, bill_id):
    """This method is executed when the user saves the updated bill info on the form page]

    Arguments:
        request
        bill_id

    Returns:
        User is redirected to cycle detail page for the selected cycle.
    """
    bill = Bills.objects.get(pk=bill_id)
    bill.name = request.POST['name']
    bill.amount = request.POST['amount']
    bill.save()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(bill.cycle.id,)))


def deleteBill(request, bill_id):
    '''

    Summary: This function grabs the bill associated with the bill_id from the Bills table.

     After that it deletes bill from the table

    Arguments:
     request: Brings back the contents of the template.
     recurring_id: Brings back the id of the current bill.

    Returns:
     HttpResponseRedirect: User is redirected to cycle detail page for the selected cycle.

    '''
    bill = Bills.objects.get(pk=bill_id)
    bill.delete()
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(bill.cycle.id,)))


def addRecurringFormDetail(request, cycle_id):
    '''Summary: retrieves all bills for the cycle in use and sends to context

    Arguments:
        request
        cycle_id

    Returns:
        Return sends context to the Add Recurring Form Detail template
    '''

    cycle = get_object_or_404(Cycle, pk=cycle_id)
    context = {'cycle': cycle}
    return render(request, 'cycles/addRecurringFormDetail.html', context)


def addRecurringDetail(request, cycle_id):
    """This method is executed when the user saves the recurring bill for a cycle on the form page]

    Arguments:
        request

    Returns:
        User is redirected to cycle detail page for the cycle currently being worked on.
    """
    managerId = request.user.id
    name = request.POST['name']
    amount = request.POST['amount']
    new_bill = Bills.objects.create(
        name=name,
        amount=amount,
        recurring=1,
        cycle=Cycle.objects.get(pk=cycle_id),
        manager=User.objects.get(pk=managerId)
    )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle_id, )))


def addOneTimeForm(request, cycle_id):
    '''Summary: retrieves all bills for the cycle in use and sends to context

    Arguments:
        request
        cycle_id

    Returns:
        Return sends context to the Add One-Time Form Detail template
    '''
    cycle = get_object_or_404(Cycle, pk=cycle_id)
    context = {'cycle': cycle}
    return render(request, 'cycles/addOneTimeForm.html', context)


def addOneTime(request, cycle_id):
    """This method is executed when the user saves the one-time bill for a cycle on the form page]

    Arguments:
        request

    Returns:
        User is redirected to cycle detail page for the cycle currently being worked on.
    """
    managerId = request.user.id
    name = request.POST['name']
    amount = request.POST['amount']
    new_tenant = Bills.objects.create(
        name=name,
        amount=amount,
        recurring=0,
        cycle=Cycle.objects.get(pk=cycle_id),
        manager=User.objects.get(pk=managerId)
    )
    return HttpResponseRedirect(reverse('cycles:cycleDetail', args=(cycle_id, )))
