from django.db.models.signals import post_save

from .models import Config, Result


def post_save_handler(sender, instance, **kwargs):

    try:
        # Update latest result for each Config
        c = Config.objects.get(host=instance.host, event=instance.event)
        c.latest = instance
        c.save()
    except Config.DoesNotExist, e:
        pass


post_save.connect(post_save_handler, sender=Result)
