# coding: utf-8
from mock import MagicMock, patch
from django.test import TestCase
from concrete_datastore.api.v1.signals import send_email, build_absolute_uri
from django.test import override_settings


@override_settings(DEBUG=True)
class SignalTests(TestCase):
    def test_build_absolute_uri(self):
        self.assertEqual(
            build_absolute_uri(uri='/uri'), 'http://testserver:80/uri'
        )

    def test_send_mail_failure_unable_to_send(self):
        patch(
            'concrete_datastore.api.v1.signals.prepare_email',
            side_effect=Exception,
        ).start()
        instance = MagicMock()
        instance.resource_status = 'to-send'
        instance.subject = 'subject'
        instance.body = 'body'
        instance.created_by = 'sender'
        send_email(sender='', instance=instance)
        patch.stopall()
