"""
Форма заявки исполнителю («оставить заявку» в анкете мастера).

Поля: имя, телефон, сообщение, согласие на обработку данных
и скрытая ловушка website для ботов.
"""

from django import forms
from django.core.validators import RegexValidator

from .models import Lead


# Телефон считаем «похожим на телефон»: плюс/цифры/пробелы/дефисы, 10–18 знаков.
# Жёсткую маску не ставим — люди пишут номера по-разному, а нам важнее не потерять клиента.
phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{10,18}$',
    message='Похоже, номер неполный — проверьте его.',
)

# Текст чекбокса согласия со ссылкой на политику (страница /privacy/).
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
    # Honeypot: человек поле не видит, бот заполнит — заявка уйдёт мимо.
    website = forms.CharField(
        required=False,
        label='',
        widget=forms.HiddenInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}),
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


from django import forms  # noqa: повторный импорт безопасен
from .models import City, Executor, Service  # noqa: то же самое


class ExecutorProfileForm(forms.ModelForm):
    """Анкета мастера: правит только владелец, только витринные поля."""

    class Meta:
        model = Executor
        fields = ('specialty', 'phone', 'price_from', 'city', 'services', 'description')
        widgets = {
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'price_from': forms.NumberInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'services': forms.CheckboxSelectMultiple,
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
