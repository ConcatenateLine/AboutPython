from datetime import datetime, timedelta
from calendar import HTMLCalendar
from ..models import Objetive

class FormatCalendar(HTMLCalendar):
	def __init__(self, user, year=None, month=None):
		self.year = year
		self.month = month
		self.user = user
		super(FormatCalendar, self).__init__()

	# formats a day as a td
	# filter objetives by day
	def formatday(self, day, objetives):
		objetives_per_day = objetives.filter(start_time__day=day)
		d = ''
		for objective in objetives_per_day:
			d += f'<li> {objective.get_html_url} </li>'

		if day != 0:
			return f"<td class='hover:bg-[var(--button-custom-bg)] text-center w-20 h-20 border border-[var(--border-color)]'><span class='text-2xl'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, objetives):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, objetives)
		return f'<tr class="border border-[var(--border-color)]"> {week} </tr>'

	# formats a month as a table
	# filter objetives by year and month
	def formatmonth(self, withyear=False):
		objetives = Objetive.objects.filter(owner=self.user,start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		# cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'<tr><th colspan="7" class="month"></th></tr>\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, objetives)}\n'
		return cal