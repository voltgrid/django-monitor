import time

from django.db import models
from django.core.exceptions import ValidationError

from .status import ALL_STATUS, RESULT_STATUS


class DateMixin(models.Model):
    """ Model Mixin to add modification and creation datestamps """
    created = models.DateTimeField("Date Created", auto_now_add=True)
    updated = models.DateTimeField("Date Updated", auto_now=True)

    version = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # increment version on save
        self.version += 1
        super(DateMixin, self).save(*args, **kwargs)


class Host(DateMixin):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name


class Event(DateMixin):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name


class Result(models.Model):
    """ Result object """
    host = models.ForeignKey(Host)
    event = models.ForeignKey(Event)
    status = models.CharField(max_length=1, choices=RESULT_STATUS)
    description = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return "%s %s [%s]" % (self.host, self.event, self.status)

    def save(self, *args, **kwargs):
        if not self.status in ALL_STATUS:
            raise ValidationError('Status not valid')
        super(Result, self).save(*args, **kwargs)


class Config(DateMixin):
    """ Host Event Config """
    host = models.ForeignKey(Host)
    event = models.ForeignKey(Event)
    timeout = models.PositiveIntegerField(help_text='Seconds')
    keep = models.PositiveIntegerField(help_text='Results to keep')
    latest = models.ForeignKey(Result, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (('host', 'event'),)
        ordering = ['host', 'event']

    def __unicode__(self):
        return "%s [%s]" % (self.host, self.event)

    def is_fresh(self):
        now = int(time.time())
        if self.latest is not None:
            latest = int(self.latest.timestamp.strftime('%s'))
            if latest + self.timeout < now:
                return False
            else:
                return True
        else:
            return False
    is_fresh.boolean = True  # Attribute for django admin (makes for pretty icons)