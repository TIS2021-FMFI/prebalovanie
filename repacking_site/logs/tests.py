from django.test import TestCase

from .models import Log
from django.contrib.auth.models import User

import datetime


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

    def test_order_logs(self):
        text1 = "abc"
        time1 = datetime.datetime(2014, 10, 10)
        log1 = Log(text=text1)
        log1.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text1).update(action_time=time1)
        log1.created = time1

        text2 = 'xyz'
        time2 = datetime.datetime(2012, 12, 12)
        log2 = Log(text=text2)
        log2.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text2).update(action_time=time2)
        log1.created = time2

        logs = Log.filter_and_order_logs_by_get({})
        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get({'order_by': 'text'})
        self.assertEquals(logs[0], log1)
        self.assertEquals(logs[1], log2)
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get(
            {'order_by': 'takyto_field_neexistuje'})

        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

    def test_order_reverse_logs(self):
        text1 = "abc"
        time1 = datetime.datetime(2010, 10, 10)
        log1 = Log(text=text1)
        log1.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text1).update(action_time=time1)
        log1.created = time1

        text2 = 'xyz'
        time2 = datetime.datetime(2014, 12, 12)
        log2 = Log(text=text2)
        log2.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text2).update(action_time=time2)
        log1.created = time2

        logs = Log.filter_and_order_logs_by_get({'order_by': '-text'})
        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get({'order_by': '-action_time'})
        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

    def test_filter_logs(self):
        text1 = "abcd"
        priority1 = Log.Priority.TRACE
        app1 = Log.App.REPACKING
        log1 = Log(text=text1, priority=priority1, app=app1)
        log1.save()

        sku2 = 'bcde'
        priority2 = Log.Priority.ERROR
        app2 = Log.App.LOGGING
        standard2 = Log(text=sku2, priority=priority2, app=app2)
        standard2.save()

        logs = Log.filter_and_order_logs_by_get({'text': 'a'})
        self.assertEquals(logs[0], log1)
        self.assertEquals(len(logs), 1)

        logs = Log.filter_and_order_logs_by_get({'text': 'bcd'})
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get({'priority': 'trace'})
        self.assertEquals(logs[0], log1)
        self.assertEquals(len(logs), 1)

        logs = Log.filter_and_order_logs_by_get({'priority': 'TRACE'})
        self.assertEquals(logs[0], log1)
        self.assertEquals(len(logs), 1)

        logs = Log.filter_and_order_logs_by_get({'app': 'I'})
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get({'app': 'bla-bla'})
        self.assertEquals(len(logs), 0)

        logs = Log.filter_and_order_logs_by_get({'nepodstany': 'zaznam'})
        self.assertEquals(len(logs), 2)
