from django import forms

from .models import Order, Response


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'city', 'service', 'budget', 'contact_name', 'phone', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('message', 'price')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Коротко: что умеете, когда можете подъехать'}),
        }
