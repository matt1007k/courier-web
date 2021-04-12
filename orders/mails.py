from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

class Mail:

    @staticmethod
    def send_complete_order(order, user):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('orders/mails/complete.html')
        content = template.render({
            'order': order,
            'user': user
        })

        message = EmailMultiAlternatives(
            subject, 
            'Mensaje importante',
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()