from django import forms
from django.contrib.auth.models import User
from .models import MedicationReminder

GLOBAL_LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('es', 'Español (Spanish)'),
    ('fr', 'Français (French)'),
    ('pt', 'Português (Portuguese)'),
    ('sw', 'Kiswahili (Swahili)'),
    ('xh', 'isiXhosa'),
    ('zu', 'isiZulu'),
    ('af', 'Afrikaans'),
    ('st', 'Sesotho'),
    ('ar', 'العربية (Arabic)'),
    ('zh', '中文 (Chinese)'),
    ('hi', 'हिन्दी (Hindi)'),
]

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-600', 'placeholder': 'e.g. Nomsa'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-600', 'placeholder': 'e.g. Dlamini'}))
    username = forms.CharField(help_text="Phone number or unique ID", widget=forms.TextInput(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-600', 'placeholder': '0821234567'}))
    preferred_language = forms.ChoiceField(choices=GLOBAL_LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-600'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-600', 'placeholder': '••••••••'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-600', 'placeholder': '••••••••'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match / Amagama osuku awahambelani.")
        return cleaned_data

class MedicationReminderForm(forms.ModelForm):
    class Meta:
        model = MedicationReminder
        fields = ['medication_name', 'scheduled_time', 'instructions']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-500', 'placeholder': 'e.g. Daily ARV Pill'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-500'}),
            'instructions': forms.Textarea(attrs={'rows': 2, 'class': 'w-full border border-purple-200 rounded-xl px-4 py-2 text-sm bg-purple-50/50 focus:outline-none focus:border-purple-500', 'placeholder': 'Take with water'}),
        }