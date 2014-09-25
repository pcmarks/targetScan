__author__ = 'pcmarks'

from django import forms
from django.forms import ValidationError

class TargetScanForm(forms.Form):
    def clean(self):
        if not self.cleaned_data.get('miRNA'):
            raise ValidationError(
                "Please enter some miRNA symbols."
            )
        return self.cleaned_data

    miRNA = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    maximum_no_of_genes = forms.IntegerField(initial=30, min_value=1, required=True,
                                             widget=forms.NumberInput(attrs={"style": "width: 4em"}))
    maximum_no_of_occurrences = forms.IntegerField(initial=30, min_value=1, required=True,
                                                   widget=forms.NumberInput(attrs={"style": "width: 4em"}))
    context_score_threshold = forms.FloatField(required=True, initial=0.0,
                                               widget=forms.TextInput(attrs={'style': 'width:4em'}))

