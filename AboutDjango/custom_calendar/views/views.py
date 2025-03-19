import calendar
from datetime import datetime, timedelta, date
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, reverse
from django.utils.safestring import mark_safe
from django.views import generic
from django.contrib import messages

from custom_calendar.actions import CustomCalendarActions
from custom_calendar.forms.add_objective import AddObjectiveForm

from ..models import Objetive
from ..utils import FormatCalendar, CustomFormatCalendar

# Create your views here.
class index( generic.ListView ):
    model = Objetive
    template_name = "custom_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = None

        mycalendar = CustomCalendarActions(self.request.user)
        
        # cal = FormatCalendar(d.year, d.month-1)
        # html_cal = cal.formatmonth(withyear=True)
        
        if mycalendar.get_calendar().format =='Table':
            cal = FormatCalendar(self.request.user, d.year, d.month)
        else:
            cal = CustomFormatCalendar(self.request.user, d.year, d.month)
        
        cal.setfirstweekday(6)
        html_cal = cal.formatmonth()

        # cal = FormatCalendar(2025, d.month+1)
        # html_cal += cal.formatmonth(withyear=True)
        context['months'] = list(calendar.month_name)[1:]
        context['current_month'] = d.month
        context['year'] = d.year
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['calendar_format'] = mycalendar.get_calendar().format
        context['add_objective'] = reverse('calendar:objective_new')
        context['goToMonth'] = reverse('calendar:index')
        context['change_format'] = reverse('calendar:change_format')
        
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = '?month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = '?month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, objective_id=None):
    instance: Objetive = None
    image = None
    initial = {}
    goToCalendar = reverse('calendar:index')
    goToDelete = reverse('calendar:objective_delete', args=(objective_id,))

    if objective_id:
        instance = get_object_or_404(Objetive, pk=objective_id)
    else:
        instance = Objetive()

    initial['themes'] = ",".join(list(instance.themes.all().values_list('name', flat=True)))
    if instance.image:      
        initial['image'] = instance.image.image.url
    
    form = AddObjectiveForm(request.POST or None, request.FILES or None, instance=instance, initial=initial)
        
    if request.POST and form.is_valid():
        if 'image' in request.FILES:
            image = request.FILES['image']
       
        try:
            custom_calendar = CustomCalendarActions(request.user, themes=form.cleaned_data['themes'])
            custom_calendar.add_objetives(request.user, form.cleaned_data, image, objective_id)

            if objective_id:
                messages.success(request, 'You have updated an objective.')
            else:
                messages.success(request, 'You have added a new objective.')
            
            return HttpResponseRedirect(reverse('calendar:index'))
        except Exception as e:
            if hasattr(e,'messages'):
                messages.error(request, str(",".join(e.messages)))
            else:
                messages.error(request, str(e))
        
    return render(request, 'add_objective.html', {'form': form, 'objective_id': objective_id, 'goToCalendar': goToCalendar, 'goToDelete': goToDelete})

def delete_objetive(request, objective_id=None):
        try:
            custom_calendar = CustomCalendarActions(request.user)
            custom_calendar.delete_objetive(request.user, objective_id)
            messages.success(request, 'You have deleted an objective.')
            return HttpResponseRedirect(reverse('calendar:index'))
        except Exception as e:
            if hasattr(e, 'messages'):
                messages.error(request, str(','.join(e.messages)))
            else:
                messages.error(request, str(e))

            return HttpResponseRedirect(reverse('calendar:objective_edit', args=(objective_id,)))

def show_objective(request, objective_id=None):
    instance = get_object_or_404(Objetive, pk=objective_id)
    image = None
    
    if instance.image:
        image = instance.image.image.url
        
    edit_url = reverse('calendar:objective_edit', args=(objective_id,))
    
    return render(request, 'show_objective.html', {'objective': instance, 'image': image, 'edit_url': edit_url})

def change_format(request):
    custom_calendar = CustomCalendarActions(request.user)
    custom_calendar.change_format(request.user)
    
    return HttpResponseRedirect(reverse('calendar:index'))
