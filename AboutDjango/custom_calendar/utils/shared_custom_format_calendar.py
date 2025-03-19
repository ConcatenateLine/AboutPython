from datetime import datetime, timedelta
from calendar import HTMLCalendar,weekday

from django.urls import reverse

from ..models import CustomCalendar, Objetive

import math

class SharedCustomFormatCalendar(HTMLCalendar):
	calendar: CustomCalendar | None = None
	name_day = {
		0: 'Monday',
		1: 'Tuesday',
		2: 'Wednesday',
		3: 'Thursday',
		4: 'Friday',
		5: 'Saturday',
		6: 'Sunday'
	}
 
	def __init__(self, user, year=None, month=None, calendar=None):
		self.year = year
		self.month = month
		self.user = user
		self.calendar = calendar
		super(SharedCustomFormatCalendar, self).__init__()

	def formatday(self, day, objetives):
		objetives_per_day = objetives.filter(start_time__day=day)
		d = ''
		t = ''
		base_characters_per_line = 25
		base_lines_per_square = 4
		current_square_size = 11
		width_day = 0
		height_day = 0
		columns_rows = math.ceil(math.sqrt(len(objetives_per_day)))
  
		if columns_rows < 1:
			columns_rows = 1

		square_width_elements = []
		square_height_elements = []
  
		for index, objective in enumerate(objetives_per_day):
			num_characters = len(objective.title)
			lines = num_characters / base_characters_per_line

			width_objective = math.ceil((lines / base_lines_per_square)) * current_square_size;   
			height_objective = math.ceil((lines / base_lines_per_square)) * current_square_size;

			if len(square_width_elements) < columns_rows:
				square_width_elements.append(width_objective)
				square_height_elements.append(height_objective)

			
			if len(square_width_elements) == columns_rows or index == len(objetives_per_day) - 1:
				sum_width = sum(square_width_elements)
				if sum_width > width_day:
					width_day = sum_width
     
				height_day += max(square_height_elements)

				square_width_elements = []
				square_height_elements = []

			
			for index, theme in enumerate(objective.themes.all()):
				t += f'<div class="absolute bottom-0 left-[{index*10}px] w-[10px] h-[10px] bg-[{ theme.color }]"></div>'
    
			url_show = reverse('calendar:shared_objective_show', args=(self.calendar.slug, objective.uuid))

			d += f'<div class="w-[{width_objective}rem] h-[{height_objective}rem] p-2 content-center relative">{objective.title} <br/> <span id="openModal" class="open_modal bg-[var(--body-quiet-color)] px-2 rounded cursor-pointer text-[var(--header-link-color)] hover:text-[var(--button-custom-hover-bg)]" name="{url_show}">Show ⇰</span>{t} {t}</div>'

			t = ''

		if day != 0:
			return f"<div class='flex flex-wrap relative overflow-hidden bg-[var(--body-medium-color)] calendar-day min-w-[11rem] min-h-[11rem] md:w-[{width_day + 0.5 * (columns_rows-1)}rem] md:h-[{height_day}rem]'><span class='text-2xl absolute bottom-0 right-0 p-2'> {self.name_day[weekday(self.year, self.month, day)]} {day}</span> {d} </div>"

		return f'<div class="relative w-[11rem] h-[11rem] border border-dashed border-[var(--border-color)] p-2" aria-label="{day}"></div>'

	def formatweek(self, theweek, objetives):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, objetives)
   
		return f'{week}'
 
	def formatmonth(self, withyear=False):
		if not self.calendar:
			return 'Format can not execute by calendar'

		objetives = Objetive.objects.filter(calendar=self.calendar, start_time__year=self.year, start_time__month=self.month)

		cal = f'<div class="w-full flex flex-wrap gap-2">'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, objetives)}\n'
		cal += '</div>'
		return cal