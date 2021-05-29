from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site

from authentication.utils import generate_token

class Mail:

    @staticmethod
    def send_verify_account_email(user, request):
        subject = 'Activación de cuenta'
        template = get_template('auth/mails/verify-account.html')
        current_year = datetime.now().year
        uid = urlsafe_base64_encode(force_bytes(user.pk)) 
        token = generate_token.make_token(user)
        domain = get_current_site(request)
        protocol = request.scheme

        content = template.render({
            'user': user,
            'domain': domain,
            'protocol': protocol,
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
    def send_complete_order(detail, full_name, email, request):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('orders/mails/complete-order.html')
        current_year = datetime.now().year
        domain = get_current_site(request)
        protocol = request.scheme

        content = template.render({
            'full_name': full_name,
            'detail': detail,
            'current_year': current_year,
            'domain': domain,
            'protocol': protocol,
        })

        message = EmailMultiAlternatives(
            subject, 
            'Mensaje de Cuy Click - Perú',
            settings.EMAIL_HOST_USER,
            [email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()