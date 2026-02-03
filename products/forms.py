

from django import forms
from .models import Product, Issue, Return

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'unit_price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['issued_quantity']
        widgets = {
            'issued_quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['return_quantity']
        widgets = {
            'return_quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }