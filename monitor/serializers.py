from rest_framework import serializers

from .models import Event, Host, Result
from .status import ALL_STATUS


class ResultSerializer(serializers.Serializer):
    host = serializers.CharField(max_length=128)
    event = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=128)
    status = serializers.CharField(max_length=1)

    def validate_status(self, attrs, status):
        """
        Check that the status is valid
        """
        if not attrs[status] in ALL_STATUS:
            raise serializers.ValidationError('Status not valid')
        return attrs

    def validate_host(self, attrs, host):
        """
        Check that the host is valid
        """
        try:
            Host.objects.get(name=attrs['host'])
        except Host.DoesNotExist, e:
            raise serializers.ValidationError('Host not valid')
        return attrs

    def validate_event(self, attrs, event):
        """
        Check that the event is valid
        """
        try:
            Event.objects.get(name=attrs['event'])
        except Event.DoesNotExist, e:
            raise serializers.ValidationError('Event not valid')
        return attrs

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            r = Result.objects.get(host=attrs['host'], event=attrs['event'])
            r.description = attrs.get('description', instance.description)
            r.status = attrs.get('status', instance.status)
            return r
        else:
            host = Host.objects.get(name=attrs['host'])
            event = Event.objects.get(name=attrs['event'])
            return Result(host=host, event=event, description=attrs['description'], status=attrs['status'])