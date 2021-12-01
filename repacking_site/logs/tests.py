from django.test import TestCase

from .models import Log
from django.contrib.auth.models import User


class LogModelTests(TestCase):

    def test_make_log(self):
        user = User.objects.create_user('john', 'johns@email.com', 'johnpassword')
        user.save()
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test")

        self.assertEqual(1, len(Log.objects.all()))

    def test_make_multiple_logs(self):
        user = User.objects.create_user('john', 'johns@email.com', 'johnpassword')
        user.save()
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test0")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test1")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test2")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test3")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test4")

        self.assertEqual(5, len(Log.objects.all()))

        self.assertRaises(Exception, Log.objects.get, text=f"Logging test6")
