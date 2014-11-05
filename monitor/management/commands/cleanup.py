from django.core.management.base import BaseCommand, CommandError

from monitor.models import *


class Command(BaseCommand):
    help = 'Delete old events'

    def handle(self, *args, **options):

        for config in Config.objects.all():

            objects_delete = Result.objects.filter(host=config.host, event=config.event)[config.keep:]

            for obj in objects_delete:
                print 'Deleting %s' % str(obj.id)
                obj.delete()