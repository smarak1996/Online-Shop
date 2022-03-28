from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

        widgets = {
            'first_name' : forms.TextInput(attrs = {'class' : 'form-control', 'style' : 'margin-bottom : -15px'}),
            'last_name' : forms.TextInput(attrs = {'class' : 'form-control', 'style' : 'margin-bottom : -15px'}),
            'email' : forms.EmailInput(attrs = {'class' : 'form-control', 'style' : 'margin-bottom : -15px'}),
            'address' : forms.TextInput(attrs = {'class' : 'form-control', 'style' : 'margin-bottom : -15px'}),
            'postal_code' : forms.TextInput(attrs = {'class' : 'form-control', 'style' : 'margin-bottom : -15px'}),
            'city' : forms.TextInput(attrs = {'class' : 'form-control', 'style' : 'margin-bottom : -15px'}),

        }