from django import forms
from django.forms import ModelForm
from .models import Candidate


class RegisterForm(ModelForm):
    accept_terms_and_conditions = forms.BooleanField(required=True, label="Ich habe die Datenschutzerklärung gelesen und stimme dieser zu",
                                                     help_text="<a href='https://aerospace-lab.de/datenschutz/' target='_blank'>Du kannst diese hier lesen</a>")
    accept_covid = forms.BooleanField(required=True, label="Ich/meine Erziehungsberechtigen akzeptiere/n die Corona Erklärung des AEROSPACE LAB.<br>\
                                                            Bitte die Erklärung ausgefüllt und unterschrieben am 1. Kurstag mitbringen oder vorab per scan an info@aerospace-lab.de!",
                                      help_text="<a href='https://aerospace-lab.de/gesundheit/' target='_blank'>Die Erkärung findest du hier</a>")

    class Meta:
        model = Candidate
        fields = ['student', 'forename', 'surname', 'email', 'phone_number',
                  'school', 'school_class', 'address', 'text']
        widgets = {
            'forename': forms.TextInput(attrs={'placeholder': 'Max'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Mustermann'}),
            'email': forms.TextInput(attrs={'placeholder': 'max.mustermann@provider.example'}),
            'school': forms.TextInput(attrs={'placeholder': 'Schulname'}),
            'school_class': forms.TextInput(attrs={'placeholder': 'z.B.: 5c, 10a, J2, Student'}),
        }


class RegisterFormWithPrevMembership(RegisterForm):
    requires_previous_year_membership = forms.BooleanField(
        required=True, label="Ich habe letztes Jahr an einem in den Voraussetzungen genannten Projekt teilgenommen")
