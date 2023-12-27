from django import forms

from estoreapp.models import Customerprofile




class CustomerprofileForm(forms.ModelForm):
    class Meta:
        model = Customerprofile
        fields = ['Name', 'Address', 'City', 'Mobile', 'Pincode', 'State']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'City': forms.TextInput(attrs={'class': 'form-control'}),
            'Mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'Pincode': forms.NumberInput(attrs={'class': 'form-control'}),
            'State': forms.Select(attrs={'class': 'form-control'})
        }