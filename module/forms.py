from django import forms

from module.models import Module

class NewModuleForm(forms.ModelForm):
    """docstring for NewModuleForm."""
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    hours = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)

    class Meta:
        model = Module
        fields = ('title', 'hours')
