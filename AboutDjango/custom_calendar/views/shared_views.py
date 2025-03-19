import calendar
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.views import generic
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
from django.views.generic import edit

from users.decorators import public_path
from custom_calendar.forms.add_calendar import AddCalendarForm
from custom_calendar.models import CustomCalendar, Objetive
from custom_calendar.utils import SharedFormatCalendar, SharedCustomFormatCalendar
from custom_calendar.actions import CustomSharedCalendarActions
from custom_calendar.forms.add_objective import AddObjectiveForm

@public_path
class show_calendar( generic.ListView ):
    model = CustomCalendar
    template_name = "custom_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_slug = self.kwargs['calendar_slug']
        d = get_date(self.request.GET.get('month', None))

        cal = None
        
        try:
            if not calendar_slug:
                raise ValidationError('Calendar slug is required')
        
            mycalendar = CustomSharedCalendarActions(self.request.user, calendar_slug)        
            
            if mycalendar.get_calendar().format =='Table':
                cal = SharedFormatCalendar(self.request.user, d.year, d.month, mycalendar.get_calendar())
            else:
                cal = SharedCustomFormatCalendar(self.request.user, d.year, d.month, mycalendar.get_calendar())
            
            cal.setfirstweekday(6)
            html_cal = cal.formatmonth()

        except Exception as e:
            messages.error(self.request, str(e))
            return context
        
        context['months'] = list(calendar.month_name)[1:]
        context['current_month'] = d.month
        context['year'] = d.year
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d, calendar_slug)
        context['next_month'] = next_month(d, calendar_slug)
        context['calendar_format'] = mycalendar.get_calendar().format
        context['add_objective'] =  'objective/new'
        context['goToMonth'] = reverse('calendar:show_calendar', args=(calendar_slug,))
        context['change_format'] = reverse('calendar:shared_change_format', args=(calendar_slug,))
        context['calendar_new'] = reverse('calendar:shared_calendar_new', args=(calendar_slug,))
        context['is_owner'] = mycalendar.is_owner(self.request.user)
        context['goToOthersCalendars'] = reverse('calendar:shared_others_calendars', args=(calendar_slug,))
        
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d, calendar_slug = ''):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month =  'shared/' + calendar_slug + '/?month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d, calendar_slug = ''):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'shared/' + calendar_slug + '/?month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def shared_event(request, calendar_slug=None, objective_id=None):
    instance: Objetive = None
    image = None
    initial = {}
    goToCalendar = reverse('calendar:show_calendar', args=(calendar_slug,))
    goToDelete = reverse('calendar:shared_objective_delete', args=(calendar_slug, objective_id))

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
            custom_calendar = CustomSharedCalendarActions(request.user, calendar_slug, themes=form.cleaned_data['themes'])
            custom_calendar.add_objetives(request.user, form.cleaned_data, image, objective_id)

            if objective_id:
                messages.success(request, 'You have updated an objective.')
            else:
                messages.success(request, 'You have added a new objective.')
            
            return HttpResponseRedirect(reverse('calendar:show_calendar', args=(calendar_slug,)))
        except Exception as e:
            if hasattr(e,'messages'):
                messages.error(request, str(",".join(e.messages)))
            else:
                messages.error(request, str(e))
        
    return render(request, 'add_objective.html', {'form': form, 'objective_id': objective_id, 'goToCalendar': goToCalendar, 'goToDelete': goToDelete})

def shared_delete_objetive(request, calendar_slug=None, objective_id=None):
        try:
            custom_calendar = CustomSharedCalendarActions(request.user, calendar_slug)
            custom_calendar.delete_objetive(request.user, objective_id)
            messages.success(request, 'You have deleted an objective.')
            return HttpResponseRedirect(reverse('calendar:show_calendar', args=(calendar_slug,)))
        except Exception as e:
            if hasattr(e, 'messages'):
                messages.error(request, str(','.join(e.messages)))
            else:
                messages.error(request, str(e))

            return HttpResponseRedirect(reverse('calendar:shared_objective_edit', args=(calendar_slug, objective_id,)))

def shared_show_objective(request, calendar_slug=None, objective_id=None):
    instance = get_object_or_404(Objetive, pk=objective_id)
    image = None
    
    if instance.image:
        image = instance.image.image.url

    edit_url = reverse('calendar:shared_objective_edit', args=(calendar_slug, objective_id))
    is_owner = instance.owner == request.user
    
    return render(request, 'show_objective.html', {'objective': instance, 'image': image, 'edit_url': edit_url, 'is_owner': is_owner})

def shared_change_format(request, calendar_slug=None):
    try:
        if not calendar_slug:
            raise ValidationError('Calendar not found')
        
        custom_calendar = CustomSharedCalendarActions(request.user, calendar_slug)
        custom_calendar.change_format(request.user)
        
        return HttpResponseRedirect(reverse('calendar:show_calendar', args=(calendar_slug,)))
    except Exception as e:
        if hasattr(e, 'messages'):
            messages.error(request, str(','.join(e.messages)))
        else:
            messages.error(request, str(e))
        
        return HttpResponseRedirect(reverse('calendar:show_calendar', args=(calendar_slug,)))

def shared_calendar_new(request, calendar_slug=None):
    instance:CustomCalendar = None
    initial = {}
    goToCalendar = reverse('calendar:show_calendar', args=(calendar_slug,))
    
    form = AddCalendarForm(request.POST or None,instance=instance, initial=initial)
        
    if request.POST and form.is_valid():
        try:
            name = form.cleaned_data['name']
            
            if not name:
                raise ValidationError('Name is required')
            
            slug = slugify(name)
            exists = CustomCalendar.objects.filter(slug=slug).exists()
            
            if exists:
                raise ValidationError('Calendar with this name already exists')
            
            calendar = CustomCalendar.objects.create(name=name, owner=request.user, is_public=True)

            messages.success(request, 'This calendar has been created successfully.')
            
            return HttpResponseRedirect(reverse('calendar:show_calendar', args=(calendar.slug,)))
        except Exception as e:
            if hasattr(e,'messages'):
                messages.error(request, str(",".join(e.messages)))
            else:
                messages.error(request, str(e))
        
    return render(request, 'add_calendar.html', {'form': form, 'goToCalendar': goToCalendar})

def shared_others_calendars(request, calendar_slug=None):
    goToCalendar = reverse('calendar:show_calendar', args=(calendar_slug,))
    calendars = []
    
    try:
        calendars = CustomCalendar.objects.filter(owner=request.user).exclude(name='Calendar')
    
        return render(request, 'others_calendars.html', {'goToCalendar': goToCalendar, 'calendars': calendars})
    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'others_calendars.html', {'goToCalendar': goToCalendar, 'calendars': calendars})