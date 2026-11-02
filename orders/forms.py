from django import forms

from .models import Order, Response

CONSENT_LABEL = (
    'Я согласен с <a href="/privacy/" target="_blank">'
    'обработкой персональных данных</a>'
)


class OrderForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label=CONSENT_LABEL,
        error_messages={'required': 'Без согласия на обработку данных заказ не размещается.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

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
