from django import forms

from .models import Rider


class PredictForm(forms.Form):
    riders = forms.ModelMultipleChoiceField(
        queryset=Rider.objects.all(),
        widget=forms.CheckboxSelectMultiple,   # or forms.SelectMultiple for a multi-select list
        label="Fav",
    )
    auto_on = forms.BooleanField(initial=True, label="Auto Calculation based on KPs")
    current_form = forms.BooleanField(initial=True, label="Current Form")
