import base64
import os

from django.conf.global_settings import ALLOWED_HOSTS
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid.helpers.mail import Attachment, Disposition, FileContent, FileName, FileType, Mail, To
from sendgrid.sendgrid import SendGridAPIClient

from MGL import settings
from MGL.settings import EMAIL_FEATURE, SENDGRID_API_KEY, SENDGRID_SENDER_EMAIL, SENDGRID_SENDER_NAME, URL_DOMAIN, URL_PROTOCOL
from .log_utils import LogUtils

'''
Classe générique de gestion des emails : identification du template, envoie de mail générique et spécifiques.
'''


class EmailUtils:

    @staticmethod
    def init_context(**kwargs):
        context = {'URL_BASE': f'{URL_PROTOCOL}://{URL_DOMAIN}'}
        context.update(**kwargs)
        return context

    # Méthode de récupération des templates.
    @staticmethod
    def render_template(template_path, context):
        custom_tpl_path = os.path.join(settings.BASE_DIR, 'templates/mails/', template_path)
        return render_to_string(custom_tpl_path, context)

    # Méthode générique d'envoie de mail.
    @staticmethod
    def send_mail(subject, recipients, from_email=None, body_html=None, attachments=None):
        if not EMAIL_FEATURE:
            LogUtils.debug("EMAIL_FEATURE=False, impossible d'envoyer des mails !")
            return

        try:
            # Initialisation du mail.
            LogUtils.debug(f'Préparation du mail {subject}, destinataires : {recipients}')
            message = Mail(from_email=from_email or To(SENDGRID_SENDER_EMAIL, SENDGRID_SENDER_NAME), to_emails=recipients, subject=subject, html_content=body_html)

            # Gestion des pièces jointes.
            if attachments and len(attachments) > 0:
                for attachment in attachments:
                    with open(attachment, 'rb') as f:
                        data = f.read()
                        f.close()
                    encoded_file = base64.b64encode(data).decode()
                    attached_file = Attachment(FileContent(encoded_file), FileName(attachment), FileType(f"application/{attachment.split('.')[-1]}"), Disposition('attachment'))
                    message.attachment = attached_file

            # Envoie du mail.
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            _response = sg.send(message)
            LogUtils.debug(f'SendGrid response : {_response.status_code}, {_response.body}')

        except Exception as e:
            LogUtils.error(f"Une erreur ({type(e).__name__}) est survenue à l'envoie du mail : {e}")
            raise e

    # Envoie du mail d'initialisation de mot de passe.
    @staticmethod
    def send_init_password_mail(user):
        LogUtils.info(f"Demande d'envoie du mail d'initialisation de mot de passe pour l'utilisateur {user.email}")

        # Initialisation du context.
        try:
            context = {
                "email": user.email,
                "domain": URL_DOMAIN,
                "user": user,
                'site_name': 'MGL',
                "protocol": URL_PROTOCOL,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
        except Exception as e:
            LogUtils.error(f'Une erreur ({type(e).__name__}) est survenue à la création du context du mail : {e}')
            raise e

        # Envoie du mail.
        EmailUtils.send_mail('Initialisation du mot de passe', [user.email], body_html=EmailUtils.render_template('core/init_password.tpl', context))

    # Envoie du mail d'export.
    @staticmethod
    def send_export_mail(recipients, attachments, subject="Export de données", context=None):
        LogUtils.debug("Demande d'envoie du mail d'export")

        # Préparation du context.
        if not context:
            context = {}
        _lp = 'send_export_mail:'
        context.update({'subject': subject})
        for attachment in attachments:
            filesize = os.path.getsize(attachment)
            if filesize > 10502564:
                context.update({'attachments': attachments})
        if context.get('attachments'):
            context.update({'base_url': ALLOWED_HOSTS[0]})
            attachments = []

        # Envoie du mail.
        EmailUtils.send_mail(subject, recipients, body_html=EmailUtils.render_template('export.tpl', context), attachments=attachments)
