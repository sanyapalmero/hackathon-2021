from django import forms

from .models import Provider


class OfferFilterForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Наименование',
        required=False
    )

    provider = forms.ModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        label='Поставщик'
    )

    date_start = forms.DateField(
        required=False,
        label='Дата от'
    )

    date_end = forms.DateField(
        required=False,
        label='Дата до'
    )

    excel = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
