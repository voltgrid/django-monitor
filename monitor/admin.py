from django.contrib import admin
from django.shortcuts import render_to_response

from admin_views.admin import AdminViews

from models import Config, Event, Host, Result


class ConfigAdmin(AdminViews):
    list_display = ('host', 'event', 'is_fresh',)
    list_filter = ('host', 'event')

    admin_views = (
        ('Event Monitoring', 'event_monitoring'),
    )

    def event_monitoring(self, *args, **kwargs):
        config = Config.objects.all()
        return render_to_response('monitor/report.html', {'config': config, })


class ResultAdmin(admin.ModelAdmin):
    list_display = ('host', 'event', 'status', 'description', 'timestamp')
    list_filter = ('host', 'event', 'status')
    date_hierarchy = 'timestamp'

admin.site.register(Config, ConfigAdmin)
admin.site.register(Event)
admin.site.register(Host)
admin.site.register(Result, ResultAdmin)