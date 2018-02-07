from django import forms
from django.core.exceptions import ValidationError


class CreateEventForm(forms.Form):
    summary = forms.CharField(
        label='Event Title',
        max_length=50
    )

    # start = forms.DateTimeField(
    #     widget=forms.DateTimeField(
    #         format("%Y-%m-%d %H:%M:%S")
    #     ),
    #     required=True
    # )
    #
    # end = forms.DateTimeField(
    #     widget=forms.DateTimeField(
    #         format("%Y-%m-%d %H:%M:%S")
    #     ),
    #     required=True
    # )

    guests = forms.Textarea()

    class Meta:
        widgets = {
            'start': forms.DateInput(format='%Y-%m-%d %H:%M:%S'),
            'end': forms.DateInput(format='%Y-%m-%d %H:%M:%S')
        }
