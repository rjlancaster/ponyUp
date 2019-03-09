from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from ..models import Recurring


def recurringlist(request):
    recurrings = Recurring.objects.all()
    context = {'recurrings': recurrings}
    return render(request, 'cycles/recurringlist.html', context)

def deleterecurring(request, recurring_id):
    '''

    Summary: This function grabs the recurring_id from the template.
     Then it seeks and selects the recurring row whose product key matches the recurring_id
     and sticks it into the recurring variable.

     After that it deletes that recurring.

    Arguments:
     request: Brings back the contents of the template.
     recurring_id: Brings back the id of the current recurring.

    Returns:
     HttpResponseRedirect: Redirects to the recurring list.

    '''
    recurring = Recurring.objects.get(pk=recurring_id)
    todaysDate = datetime.now()
    recurring.deletedOn = todaysDate
    recurring.save()
    return HttpResponseRedirect(reverse('cycles:recurringlist'))

def editrecurringForm(request, recurring_id):
    recurringRow = get_object_or_404(Recurring, pk=recurring_id)
    context = {'recurring': recurringRow}
    return render(request, 'cycles/editRecurringForm.html', context)

def editrecurring(request, recurring_id):
    """R Lancaster[This method is executed when the user saves the updated user settings on the user settings update form page]

    Arguments:
        request

    Returns:
        User is redirected to main User Settings page.
    """
    recurring = Recurring.objects.get(pk=recurring_id)
    recurring.name = request.POST['name']
    recurring.save()
    return HttpResponseRedirect(reverse('cycles:recurringlist'))

def addrecurringForm(request):
    return render(request, 'cycles/addRecurringForm.html')

def addrecurring(request):
    """R Lancaster[This method is executed when the user saves the updated user settings on the user settings update form page]

    Arguments:
        request

    Returns:
        User is redirected to main User Settings page.
    """
    name = request.POST['name']
    new_recurring = Recurring.objects.create(
        name = name,
        deletedOn = null
    )
    return HttpResponseRedirect(reverse('cycles:recurringlist'))