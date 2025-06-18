from datetime import datetime, timedelta
from calendar import HTMLCalendar

from django.urls import reverse
from ..models import CustomCalendar, Objetive

class FormatCalendar(HTMLCalendar):
	calendar: CustomCalendar | None = None
 
	def __init__(self, calendar, user, year=None, month=None):
		self.year = year
		self.month = month
		self.user = user
		self.calendar = calendar
		super(FormatCalendar, self).__init__()

	####### formats a day as a td
	# filter objetives by day
	def formatday(self, day, objetives):
		objetives_per_day = objetives.filter(start_time__day=day)
		d = ''
		t = ''
  
		for objective in objetives_per_day:
			for index, theme in enumerate(objective.themes.all()):
				t += f'<div class="absolute bottom-[{index*2}px] right-0 w-1/2 h-[2px] bg-[{ theme.color }]"></div>'
    
			url_show = reverse('calendar:objective_show', args=(objective.uuid,))
   
			d+= f'<li class="text-start relative">{objective.title} <br/> <span id="openModal" class="open_modal relative bg-[var(--body-medium-color)] px-2 rounded cursor-pointer text-[var(--accent)] hover:text-[var(--button-custom-hover-bg)]" name="{url_show}">Show ⇰</span>{t}</li>'
	
			t = ''

		if day != 0:
			return f"<td class='hover:bg-[var(--button-custom-bg)] text-center w-20 h-20 border border-[var(--border-color)]'><span class='text-2xl'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	####### formats a week as a tr
	def formatweek(self, theweek, objetives):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, objetives)
		return f'<tr class="border border-[var(--border-color)]"> {week} </tr>'

	####### formats a month as a table
	# filter objetives by year and month
	def formatmonth(self, withyear=False):
		objetives = Objetive.objects.filter(calendar=self.calendar, owner=self.user,start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar w-full">\n'
		cal += f'<tr><th colspan="7" class="month"></th></tr>\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, objetives)}\n'
		return cal 
