# notes/forms.py

from django import forms
from .models import Grade

class RubricForm(forms.ModelForm):
    ontime = forms.ChoiceField(choices=[
        (0, 'A temps'),
        (2, 'Una mica tard (-2)'),
        (4, 'Molt tard (-4)')
    ])
    quality = forms.ChoiceField(choices=[
        (0, 'Perfecta'),
        (2, 'Es podria millorar (-2)'),
        (4, 'Deficient (-4)')
    ])
    screenshot = forms.ImageField(required=False)

    class Meta:
        model = Grade
        fields = ['ontime', 'quality', 'screenshot']
