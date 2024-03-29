from django.test import TestCase

from .models import Log
from django.contrib.auth import get_user_model

import datetime


class LogModelTests(TestCase):

    def test_make_log(self):
        user = get_user_model().objects.create_user('john', 'johns@email.com', 'johnpassword')
        user.save()
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test")

        self.assertEqual(1, len(Log.objects.all()))

    def test_make_multiple_logs(self):
        user = get_user_model().objects.create_user('john', 'johns@email.com', 'johnpassword')
        user.save()
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test0")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test1")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test2")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test3")
        Log.make_log(Log.App.LOGGING, Log.Priority.TRACE, user, "Logging test4")

        self.assertEqual(5, len(Log.objects.all()))

        self.assertRaises(Exception, Log.objects.get, text=f"Logging test6")

    def test_order_logs(self):
        user1 = get_user_model().objects.create_user('cccc', 'johns@email.com', 'johnpassword', barcode='cccc')
        user1.save()
        text1 = "abc"
        time1 = datetime.datetime(2014, 10, 10)
        log1 = Log(text=text1, user=user1)
        log1.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text1).update(action_time=time1)
        log1.created = time1

        user2 = get_user_model().objects.create_user('bbbb', 'johns@email.com', 'johnpassword', barcode='bbbb')
        user2.save()
        text2 = 'xyz'
        time2 = datetime.datetime(2012, 12, 12)
        log2 = Log(text=text2, user=user2)
        log2.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text2).update(action_time=time2)
        log1.created = time2

        logs = Log.filter_and_order_logs_by_get({})
        self.assertEquals(logs[0], log1)
        self.assertEquals(logs[1], log2)
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get({'order_by': 'text'})
        self.assertEquals(logs[0], log1)
        self.assertEquals(logs[1], log2)
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get({'order_by': 'user__username'})
        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

        logs = Log.filter_and_order_logs_by_get(
            {'order_by': 'takyto_field_neexistuje'})

        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

    def test_order_reverse_logs(self):
        user1 = get_user_model().objects.create_user('bbbb', 'johns@email.com', 'johnpassword', barcode='bbbb')
        user1.save()
        text1 = "abc"
        time1 = datetime.datetime(2012, 10, 10)
        log1 = Log(text=text1, user=user1)
        log1.save()

        # workaround because of auto_now on created field
        Log.objects.filter(text=text1).update(action_time=time1)
        log1.created = time1

        user2 = get_user_model().objects.create_user('cccc', 'johns@email.com', 'johnpassword', barcode='cccc')
        user2.save()
        text2 = 'xyz'
        time2 = datetime.datetime(2018, 12, 12)
        log2 = Log(text=text2, user=user2)
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

        logs = Log.filter_and_order_logs_by_get({'order_by': '-user__username'})
        self.assertEquals(logs[0], log2)
        self.assertEquals(logs[1], log1)
        self.assertEquals(len(logs), 2)

    def test_filter_logs(self):
        user1 = get_user_model().objects.create_user('xyz', 'johns@email.com', 'johnpassword', barcode='xyz')
        user1.save()
        text1 = "abcd"
        priority1 = Log.Priority.TRACE
        app1 = Log.App.REPACKING
        log1 = Log(text=text1, priority=priority1, app=app1, user=user1)
        log1.save()

        user2 = get_user_model().objects.create_user('yz', 'johns@email.com', 'johnpassword', barcode='yz')
        user2.save()
        text2 = 'bcde'
        priority2 = Log.Priority.ERROR
        app2 = Log.App.LOGGING
        standard2 = Log(text=text2, priority=priority2, app=app2, user=user2)
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

        # logs = Log.filter_and_order_logs_by_get({'username': 'yz'})
        # self.assertEquals(len(logs), 2)

        # logs = Log.filter_and_order_logs_by_get({'username': 'xyz'})
        # self.assertEquals(len(logs), 1)

        # logs = Log.filter_and_order_logs_by_get({'username': 'meno'})
        # self.assertEquals(len(logs), 0)

        logs = Log.filter_and_order_logs_by_get({'app': 'bla-bla'})
        self.assertEquals(len(logs), 0)

        logs = Log.filter_and_order_logs_by_get({'nepodstany': 'zaznam'})
        self.assertEquals(len(logs), 2)
