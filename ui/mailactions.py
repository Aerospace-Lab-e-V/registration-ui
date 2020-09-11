import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


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
