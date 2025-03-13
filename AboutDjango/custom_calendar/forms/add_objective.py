from django.forms import DateField, ModelForm, CharField, SelectDateWidget, TextInput

from custom_calendar.models import Objetive

class AddObjectiveForm(ModelForm):
    themes = CharField(
        max_length=250,
        required=False,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter themes separated by commas',
        }),
    )
    start_time = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    end_time = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Objetive
        fields = ['title', 'description', 'start_time', 'end_time','themes']

    def __init__(self, *args, **kwargs):
        super(AddObjectiveForm, self).__init__(*args, **kwargs)
