from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from monitor.models import *

from monitor.emails import send_alert_email


class Command(BaseCommand):
    help = 'Send email alerts'

    def handle(self, *args, **options):

        results = []
        admin_emails = [v for k,v in settings.ADMINS]

        for c in Config.objects.all():
            if c.is_fresh() is False:
                results.append(c)

        if results > 0:
            # Send an alert email
            send_alert_email(recipient=admin_emails, results=results)