# import datetime
from django import forms
from dynamic_preferences.serializers import *
from dynamic_preferences.types import BasePreferenceType, BooleanPreference, StringPreference, DateTimePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


@global_preferences_registry.register
class OrganizationMailSwitch(BooleanPreference):
    name = 'organization_mail_alert'
    verbose_name = "Bei jeder neuen Anmeldung Mail-Adresse benachrichtigen"
    default = False


@global_preferences_registry.register
class RegistrationCovid(BooleanPreference):
    name = 'registration_covid'
    verbose_name = "COVID Haftungsfreistellung "
    default = False


@global_preferences_registry.register
class OrganizationMailAddress(StringPreference):
    name = 'organization_mail_address'
    verbose_name = "Mail-Adresse für Benachrichtigung"
    default = ''


@global_preferences_registry.register
class RegistrationOpeningTime(BasePreferenceType):
    field_class = forms.TimeField
    serializer = TimeSerializer
    name = 'registration_opening_time'
    verbose_name = "Zeit, ab der die Anmeldung offen steht"
    default = time(15, 00)
