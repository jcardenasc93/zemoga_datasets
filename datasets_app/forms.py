""" The forms module to capture inputs from the user """
from django import forms
from datasets_app.models import Dataset

class DatasetForm(forms.ModelForm):
    """ Model based form to create dataset """
    class Meta:
        model = Dataset
        exclude = ['_id']
