from django import forms
from django.forms import ModelForm
from .models import Candidate


class RegisterForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['student', 'forename', 'surname', 'email', 'phone_number',
                  'school', 'school_class', 'address', 'phone_number',
                  'application', 'parent_forename', 'parent_surname',
                  'parent_email']
        widgets = {
            'forename': forms.TextInput(attrs={'placeholder': 'Max'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Mustermann'}),
            'email': forms.TextInput(attrs={'placeholder': 'max.mustermann@provider.example'}),
            'school': forms.TextInput(attrs={'placeholder': 'Schulname'}),
            'school_class': forms.TextInput(attrs={'placeholder': 'z.B.: 5c, 10a, J2, Student'}),

            'parent_forename': forms.TextInput(attrs={'placeholder': 'Max'}),
            'parent_surname': forms.TextInput(attrs={'placeholder': 'Mustermann'}),
            'parent_email': forms.TextInput(attrs={'placeholder': 'max.mustermann@provider.example'}),
        }

    def __init__(self, *args, **kwargs):
        requires_previous_year_membership = kwargs.pop(
            'requires_previous_year_membership', False)
        accept_privacy = kwargs.pop(
            'accept_privacy', True)
        accept_covid = kwargs.pop(
            'accept_covid', False)
        remove_application = kwargs.pop(
            'remove_application', False)

        super(RegisterForm, self).__init__(*args, **kwargs)

        if requires_previous_year_membership:
            self.fields['requires_previous_year_membership'] = forms.BooleanField(
                required=True, label="Ich habe letztes Jahr an einem in den Voraussetzungen genannten Projekt teilgenommen")
        if accept_privacy:
            self.fields['accept_privacy'] = forms.BooleanField(
                required=True, label="Ich habe die Datenschutzerklärung gelesen und stimme dieser zu",
                help_text="<a href='https://aerospace-lab.de/datenschutz/' target='_blank'>Du kannst diese hier lesen</a>")
        if accept_covid:
            self.fields['accept_covid'] = forms.BooleanField(
                required=True, label="Ich/meine Erziehungsberechtigen akzeptiere/n die Haftungsfreistellung des AEROSPACE LAB.<br>\
                <b>Bitte die Erklärung ausgefüllt und unterschrieben am 1. Kurstag mitbringen \
                    oder vorab per scan an info@aerospace-lab.de!</b><br>\
                (Sie wird allen Teilnehmer auch noch einmal per Mail zugestellt)",
                help_text="<a href='https://aerospace-lab.de/gesundheit/' target='_blank'>Die Haftungsfreistellung findest du hier</a>")
        if remove_application:
            del self.fields['application']
