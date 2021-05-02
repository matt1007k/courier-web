from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

class Mail:

    @staticmethod
    def send_client_complete_order(order, user):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('orders/mails/client-complete-order.html')
        content = template.render({
            'order': order,
            'user': user
        })

        message = EmailMultiAlternatives(
            subject, 
            'Mensaje de Cuy Click - Perú',
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()

    @staticmethod
    def send_origin_complete_order(detail, email):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('orders/mails/origin-complete-order.html')
        content = template.render({
            'detail': detail,
        })

        message = EmailMultiAlternatives(
            subject, 
            'Mensaje de Cuy Click - Perú',
            settings.EMAIL_HOST_USER,
            [email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()