from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from news.models import City

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



def city_choices():
    """Список городов из базы: тот же, что в анкете исполнителя."""
    return [('', 'Не указан')] + [(c.name, c.name) for c in City.objects.all()]


class ProfileForm(forms.ModelForm):
    city = forms.ChoiceField(
        required=False,
        label='Город',
        choices=city_choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Profile
        fields = ('city', 'phone', 'bio', 'avatar')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {'phone': 'Телефон', 'bio': 'О себе', 'avatar': 'Аватар'}
