from django import forms
from .models import WorkSiteLocations
from django.forms import ModelChoiceField
import requests



class SiteDropDownForm(forms.Form):    
    site = forms.ModelChoiceField(queryset=None, empty_label=None)
    def __init__(self, *args, **kwargs):
        super(SiteDropDownForm, self).__init__(*args, **kwargs)
        self.fields['site'].queryset = WorkSiteLocations.objects.all()
        self.fields['site'].label_from_instance = lambda obj: "%s" % (obj.sitename)

        
    
