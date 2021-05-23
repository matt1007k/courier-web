from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError

from authentication.utils import generate_token

class Mail:

    @staticmethod
    def send_verify_account_email(user):
        subject = 'Activar tu cuenta'
        template = get_template('auth/mails/verify-account.html')
        current_year = datetime.now().year
        uid = urlsafe_base64_encode(force_bytes(user.pk)) 
        token = generate_token.make_token(user)

        content = template.render({
            'user': user,
            'uid': uid,
            'token': token,
            'current_year': current_year
        })
        
        message = EmailMultiAlternatives(
            subject,
            'Mensage de Cuy Click - Perú',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        message.attach_alternative(content, 'text/html')
        message.send()


    @staticmethod
    def send_complete_order(detail, email):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('orders/mails/complete-order.html')
        current_year = datetime.now().year
        content = template.render({
            'detail': detail,
            'current_year': current_year,
        })

        message = EmailMultiAlternatives(
            subject, 
            'Mensaje de Cuy Click - Perú',
            settings.EMAIL_HOST_USER,
            [email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()