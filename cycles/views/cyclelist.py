from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Count
from ..models import Cycle

def cyclelist(request):
    cycles = Cycle.objects.all()
    context = {'cycles': cycles}
    print('print this')
    return render(request, 'cycles/cyclelist.html', context)

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