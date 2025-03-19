from django.forms import ModelForm, ValidationError

from custom_calendar.models import CustomCalendar

class AddCalendarForm(ModelForm):

    def clean_name(self):
        name = self.cleaned_data['name']
        is_valid = len(name) >= 5

        if not name or not is_valid:
            raise ValidationError('Name must be at least 5 characters long')
        return name

    class Meta:
        model = CustomCalendar
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        super(AddCalendarForm, self).__init__(*args, **kwargs)
