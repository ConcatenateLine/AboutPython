import uuid
from django.forms import ValidationError
from custom_calendar.utils.generate import generate_green_color
from ..models import CustomCalendar, Objetive, Theme, ImageCF

class CustomCalendarActions:
    calendar = None

    def __init__(self,user, themes=None):
        try:
            self.calendar = CustomCalendar.objects.filter(owner=user).first()

            if not self.calendar:
                self.calendar = CustomCalendar.objects.create(
                    name='Calendar',
                    slug='calendar',
                    is_public=False,
                    owner=user
                ) 
            
            if themes:
                self.add_themes(themes)
            
        except CustomCalendar.DoesNotExist:
            raise CustomCalendar.DoesNotExist("CustomCalendar does not exist")
            

    def get_calendar(self):
        return self.calendar

    def add_themes(self, themes):
        if not themes or not self.calendar:
            return

        themes_list = [theme.strip() for theme in themes.split(',')]
        
        for theme in themes_list:
            theme_consult, created  = Theme.objects.get_or_create(name=theme)
            if created:
                theme_consult.color = generate_green_color()
                theme_consult.save()

        self.calendar.themes.add(theme_consult)
        
        self.calendar.save()

    def add_objetives(self, user, objetive, image=None, objective_id=None):

        new_objective = None
        image_objective = None

        if not objetive or not self.calendar:
            return

        if objective_id:
            new_objective = Objetive.objects.get(uuid=objective_id)
            new_objective.title = objetive['title']
            new_objective.description = objetive['description']
            new_objective.start_time = objetive['start_time']
            new_objective.end_time = objetive['end_time']
            new_objective.themes.clear()

        else:
            new_objective = Objetive.objects.create(
                title=objetive['title'],
                description=objetive['description'],
                start_time=objetive['start_time'],
                end_time=objetive['end_time'],
                owner=self.calendar.owner,
                calendar=self.calendar,
            )   

        if new_objective.owner != user:
            raise ValidationError('You are not authorized to update this objective.')

        if image:
            user_images_count = ImageCF.objects.filter(owner=user).count()
            max_images_limit = 20

            if user_images_count < max_images_limit:
                image.name = f'{user.username}_{uuid.uuid4()}'
                image_objective = ImageCF.objects.create(name=image.name, image=image, owner=user)
            else:
                raise ValidationError('You have reached the maximum number of images allowed.')

        if 'themes' in objetive:
            themes_list = [theme.strip() for theme in objetive['themes'].split(',')]

            for theme in themes_list:
                 new_objective.themes.add(Theme.objects.filter(name=theme).first())
        
        if image_objective:
            new_objective.image = image_objective
        
        new_objective.save()

    def delete_objetive(self, user, objective_id):
        if not objective_id or not self.calendar:
            return

        objective = Objetive.objects.get(uuid=objective_id)

        print('image')
        print(objective.image)

        if objective.owner != user:
            raise ValidationError('You are not authorized to delete this objective.')

        if objective.image:
            image = objective.image
            image.delete()

        objective.delete()
