from django import forms
from django.core.validators import RegexValidator

from .models import Lead


phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{10,18}$',
    message='Похоже, номер неполный — проверьте его.',
)

CONSENT_LABEL = (
    'Я согласен с <a href="/privacy/" target="_blank">'
    'обработкой персональных данных</a>'
)


class LeadForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=32,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+7 ___ ___-__-__',
            'class': 'lead-input',
        }),
    )
    consent = forms.BooleanField(
        required=True,
        label=CONSENT_LABEL,
        error_messages={'required': 'Без согласия на обработку данных заявку отправить нельзя.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Lead
        fields = ('name', 'phone', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'lead-input'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Что нужно сделать (например, заменить смеситель на кухне)',
                'class': 'lead-input', 'rows': 4,
            }),
        }
