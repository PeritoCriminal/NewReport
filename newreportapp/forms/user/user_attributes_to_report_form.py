# newreportapp/forms/user/user_attributes_to_report_form.py

from django import forms
from newreportapp.models import UserAttributesToReportModel

class UserAttributesToReportForm(forms.ModelForm):
    class Meta:
        model = UserAttributesToReportModel
        fields = ['user', 'director', 'state', 'city', 'unit', 'team']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
        }

    def __init__(self, *args, **kwargs):
        super(UserAttributesToReportForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
