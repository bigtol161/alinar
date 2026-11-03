from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

CONSENT_LABEL = (
    'Я согласен с <a href="/privacy/" target="_blank">'
    'обработкой персональных данных</a>'
)


class RegisterForm(UserCreationForm):
    # Honeypot: человек поле не видит, бот честолюбиво заполнит — и отсечётся
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.HiddenInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}),
    )
    consent = forms.BooleanField(
        required=True,
        label=CONSENT_LABEL,
        error_messages={'required': 'Без согласия на обработку данных аккаунт не создаётся.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta(UserCreationForm.Meta):
        pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('city', 'phone', 'bio', 'avatar')
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {'city': 'Город', 'phone': 'Телефон', 'bio': 'О себе', 'avatar': 'Аватар'}
