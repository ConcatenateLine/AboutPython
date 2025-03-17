from django.forms import DateField, FileInput, ImageField, ModelForm, CharField, SelectDateWidget, TextInput, ValidationError

from custom_calendar.models import Objetive

class AddObjectiveForm(ModelForm):
    themes = CharField(
        max_length=150,
        required=False,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter themes separated by commas',
        }),
    )
    start_time = DateField(widget=SelectDateWidget(
        attrs={
            'class': 'form-control',
            'style': 'width: 33%;'
        }
    ))
    end_time = DateField(widget=SelectDateWidget(
        attrs={
            'class': 'form-control',
            'style': 'width: 33%;'
        }
    ))
    image = ImageField(widget=FileInput(
        attrs={
            'class': 'form-control',
        }),
        required=False,
    )

    def clean_title(self):
        title = self.cleaned_data['title']
        is_valid = len(title) >= 5

        if not title or not is_valid:
            raise ValidationError('Title must be at least 5 characters long')
        return title

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not hasattr(image, 'content_type'):
            return image

        if image.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/webp']:
            raise ValidationError('Image type accepted: JPEG o PNG.')

        if image.size > 1 * 1024 * 1024:
            raise ValidationError('Image size cannot exceed 1 MB.')

        return image
 
    class Meta:
        model = Objetive
        fields = ['title', 'description', 'start_time', 'end_time','themes']

    def __init__(self, *args, **kwargs):
        super(AddObjectiveForm, self).__init__(*args, **kwargs)
