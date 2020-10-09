from dynamic_preferences.types import BooleanPreference, StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

general = Section('general')


@global_preferences_registry.register
class OrganizationMailSwitch(BooleanPreference):
    section = general
    name = 'organization_mail_alert'
    verbose_name = "Bei jeder neuen Anmeldung Mail-Adresse benachrichtigen"
    default = False


@global_preferences_registry.register
class OrganizationMailAddress(StringPreference):
    section = general
    name = 'organization_mail_address'
    verbose_name = "Mail-Adresse für Benachrichtigung"
    default = ''
