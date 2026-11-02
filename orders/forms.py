"""
Формы раздела заказов.

- OrderForm — заказчик описывает, что нужно сделать: где, за сколько,
  как с ним связаться. Согласие на обработку данных обязательно.
- ResponseForm — отклик исполнителя на чужой заказ: сообщение и цена.
  Доступна только вошедшим исполнителям, от спама защищена тем,
  что анонимов отсеивает регистрация.
"""

from django import forms

from .models import Order, Response

# Текст чекбокса согласия со ссылкой на политику (страница /privacy/).
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
    # Honeypot: человек поле не видит, бот заполнит — заказ уйдёт мимо.
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.HiddenInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}),
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
