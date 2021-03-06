import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from dynamic_preferences.registries import global_preferences_registry

logger = logging.getLogger(__name__)
global_preferences = global_preferences_registry.manager()


def successful_registration_action(candidate, project):
    ''' handles response-mail and other optional defined processes
    '''
    send_registration_confirmation_mail(candidate, project)
    if global_preferences['organization_mail_alert']:
        send_registration_alert_mail(candidate, project)


def send_registration_confirmation_mail(candidate, project):
    ''' sends the mail after a user submitted his registration
    '''
    logger.info('Start sending Mail')
    from_email = settings.EMAIL_HOST_USER

    subject = 'Projektanmeldung AEROSPACE LAB'

    context = {'name': candidate.forename,
               'groupname': project.name
               }
    msg_plain = render_to_string(
        'ui/mail-templates/confirmation-mail.txt', context)
    msg_html = render_to_string(
        'ui/mail-templates/confirmation-mail.html', context)
    try:
        send_mail(subject, msg_plain, from_email, [
            candidate.email], html_message=msg_html)
    except Exception as exception:
        logger.error('An Error occurred while sendin mail:')
        logger.error(exception)
        

def send_registration_alert_mail(candidate, project):
    ''' sends a mail to an organizer after a user submitted his registration
    '''
    logger.info('Start sending Alert-Mail')
    from_email = settings.EMAIL_HOST_USER
    to_email = global_preferences['organization_mail_address']

    subject = 'Neue Projektanmeldung auf Webseite'

    context = {'forename': candidate.forename,
               'surname': candidate.surname,
               'groupname': project.name
               }
    msg_plain = render_to_string(
        'ui/mail-templates/organization-alert-mail.txt', context)
    msg_html = render_to_string(
        'ui/mail-templates/organization-alert-mail.html', context)
    try:
        send_mail(subject, msg_plain, from_email, [
                  to_email], html_message=msg_html)
    except Exception as exception:
        logger.error('An Error occurred while sendin alert-mail:')
        logger.error(exception)
