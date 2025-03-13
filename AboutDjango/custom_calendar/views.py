import calendar
from datetime import datetime, timedelta, date
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, reverse
from django.utils.safestring import mark_safe
from django.views import generic
from django.contrib import messages

from custom_calendar.actions import CustomCalendarActions
from custom_calendar.forms.add_objective import AddObjectiveForm

from .models import Objetive
from .utils import FormatCalendar

# Create your views here.
class index( generic.ListView ):
    model = Objetive
    template_name = "custom_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        # cal = FormatCalendar(d.year, d.month-1)
        # html_cal = cal.formatmonth(withyear=True)

        cal = FormatCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)

        # cal = FormatCalendar(2025, d.month+1)
        # html_cal += cal.formatmonth(withyear=True)
        context['months'] = list(calendar.month_name)[1:]
        context['current_month'] = d.month
        context['year'] = d.year
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, objective_id=None):
    instance: Objetive = None
    if objective_id:
        instance = get_object_or_404(Objetive, pk=objective_id)
    else:
        instance = Objetive()

    form = AddObjectiveForm(request.POST or None, instance=instance, initial={
        'themes': ",".join(list(instance.themes.all().values_list('name', flat=True)))
    })
    
    if request.POST and form.is_valid():
       
        custom_calendar = CustomCalendarActions(request.user, themes=form.cleaned_data['themes'])
        custom_calendar.add_objetives(form.cleaned_data, objective_id)

        if objective_id:
            messages.success(request, 'You have updated an objective.')
        else:
            messages.success(request, 'You have added a new objective.')
        
        return HttpResponseRedirect(reverse('calendar:index'))
        
    return render(request, 'add_objective.html', {'form': form})