from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from datetime import datetime
from ..models import Recurring, User


def recurringlist(request):
    '''Summary: Captures all of the recurring bill categories from the Recurring table and sends it to context

    Arguments:
        request

    Returns:
        Renders the context to the recurringlist template.
    '''
    managerId = request.user.id
    recurrings = Recurring.objects.filter(manager=managerId)
    context = {'recurrings': recurrings}
    return render(request, 'cycles/recurringlist.html', context)

def deleteRecurring(request, recurring_id):
    '''

    Summary: This function grabs the recurring_id from the template.

     After that it submits a deleted on date into the deletedOn field.

    Arguments:
     request: Brings back the contents of the template.
     recurring_id: Brings back the id of the current recurring category.

    Returns:
     HttpResponseRedirect: Redirects to the recurring list.

    '''
    recurring = Recurring.objects.get(pk=recurring_id)
    todaysDate = datetime.now()
    recurring.deletedOn = todaysDate
    recurring.save()
    return HttpResponseRedirect(reverse('cycles:recurringlist'))

def editRecurringForm(request, recurring_id):
    '''Summary: Grabs the recurring category name associated with the ID and submits it in context to the form for editing

    Arguments:
        request
        recurring_id

    Returns:
        Renders the context to the edit Recurring Form template.
    '''

    recurringRow = get_object_or_404(Recurring, pk=recurring_id)
    context = {'recurring': recurringRow}
    return render(request, 'cycles/editRecurringForm.html', context)

def editRecurring(request, recurring_id):
    """This method is executed when the user saves the updated recurring category on the form page]

    Arguments:
        request
        recurring_id

    Returns:
        User is redirected to main recurring category list page.
    """
    recurring = Recurring.objects.get(pk=recurring_id)
    recurring.name = request.POST['name']
    recurring.save()
    return HttpResponseRedirect(reverse('cycles:recurringlist'))

def addRecurringForm(request):
    return render(request, 'cycles/addRecurringForm.html')

def addRecurring(request):
    """This method is executed when the user saves the newrecurring category on the form page]

    Arguments:
        request

    Returns:
        User is redirected to main recurring category list page.
    """
    managerId = request.user.id
    name = request.POST['name']
    new_recurring = Recurring.objects.create(
        name = name,
        manager = User.objects.get(pk=managerId)
    )
    return HttpResponseRedirect(reverse('cycles:recurringlist'))