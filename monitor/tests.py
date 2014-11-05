from django.core.exceptions import ValidationError
from django.test import TestCase

from model_mommy import mommy

from .models import Host, Event, Config, Result


# Creation Tests
class MonitorTest(TestCase):

    def test_host(self):
        host = mommy.make_recipe('monitor.host')
        self.assertTrue(isinstance(host, Host))
        return host

    def test_event(self):
        event = mommy.make_recipe('monitor.event')
        self.assertTrue(isinstance(event, Event))
        return event

    def test_config(self):
        config = mommy.make_recipe('monitor.config')
        self.assertTrue(isinstance(config, Config))
        return config

    def test_result(self):
        result = mommy.make_recipe('monitor.result')
        self.assertTrue(isinstance(result, Result))
        return result


class ResultTest(TestCase):

    def test_results(self):
        host = mommy.make_recipe('monitor.host', name='example.com')
        event = mommy.make_recipe('monitor.event', name='Example Event')
        config = mommy.make_recipe('monitor.config', host=host, event=event, keep=2)
        mommy.make_recipe('monitor.result', host=host, event=event, _quantity=10)
        self.assertTrue(isinstance(Config.objects.get(host=host, event=event).latest, Result))

    def test_invalid_status(self):
        with self.assertRaises(ValidationError):
            r = mommy.make_recipe('monitor.result', status='Z')


from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ResultAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('result-list')
        self.user = mommy.make_recipe('account.user', is_superuser=True)  # FIXME
        self.host = mommy.make_recipe('monitor.host', name='example.com')
        self.event = mommy.make_recipe('monitor.event', name='Example Event')

        self.data = {'host': self.host.name,
                     'event': self.event.name,
                     'description': 'test',
                     'status': 'O', }

        self.client.force_authenticate(user=self.user)

    def test_create_result(self):
        """
        Ensure we can create a new result object.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.data)

    def test_validate_status(self):
        """ Check that an invalid status is caught """
        data = self.data
        data['status'] = 'Z'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"status": ["Status not valid"]})