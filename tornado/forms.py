# from datetimepicker.widgets import DateTimePicker
# from bootstrap_datepicker.widgets import DatePicker
from django import forms
from django.core.exceptions import ValidationError


class CreateEventForm(forms.Form):
    summary = forms.CharField(
        label='Event Title',
        max_length=50
    )

    start = forms.DateTimeField(
        widget=forms.TextInput(),
        label="Start Time"
    )

    end = forms.DateTimeField(
        widget=forms.TextInput(),
        label="End Time"
    )

    organizer = forms.EmailField(
        label="Organizer Email"
    )

    class Meta:
        fields = ('start', 'end', 'guests', 'organizer')
        widgets = {
            'start': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
            'end': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
            'guests': forms.Textarea()
        }
