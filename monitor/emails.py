from django.conf import settings


def send_alert_email(recipient, results):

        subject = 'Monitoring Alert'
        sender = 'Monitor <monitor@example.com>'
        extra_context = {'subject': subject, 'recipient': recipient, 'results': results, 'STATIC_URL': settings.STATIC_URL, }
        #send_multipart_mail('monitor/email', extra_context, subject, recipient, sender=sender)
        raise NotImplementedError('Email functionality not implemented')
