from django import forms
from django.contrib.auth.forms import UserCreationForm

CONSENT_LABEL = (
    'Я согласен с <a href="/privacy/" target="_blank">'
    'обработкой персональных данных</a>'
)


class RegisterForm(UserCreationForm):
    consent = forms.BooleanField(
        required=True,
        label=CONSENT_LABEL,
        error_messages={'required': 'Без согласия на обработку данных аккаунт не создаётся.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta(UserCreationForm.Meta):
        pass
