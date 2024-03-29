from django.test import TestCase

from .models import *
import datetime


class RepackingStandardsModelTests(TestCase):

    def test_dummy(self):
        self.assertIs(True, True)

    def test_get_repacking_standard_by_sku(self):
        sku = "sku"
        destination = "destination"
        cofor = "cofor"
        standard = RepackingStandard(SKU=sku, COFOR=cofor, destination=destination)
        standard.save()
        for i in range(10):
            RepackingStandard(SKU=sku + str(i), COFOR=cofor, destination=destination).save()

        self.assertEqual(standard.SKU, RepackingStandard.get_standard(sku, destination).SKU)
        self.assertEqual(sku, RepackingStandard.get_standard(sku, destination).SKU)

        self.assertEqual(cofor, RepackingStandard.get_standard(sku, destination).COFOR)

        self.assertNotEqual(standard.SKU, RepackingStandard.get_standard(sku + '1', destination).SKU)
        self.assertIsNone(RepackingStandard.get_standard(sku, destination + '1'))
        self.assertIsNone(RepackingStandard.get_standard(destination, sku))

    def test_order_repacking_standard(self):
        sku1 = "a"
        cofor1 = "b"
        time1 = datetime.datetime(2014, 10, 10)
        standard1 = RepackingStandard(SKU=sku1, COFOR=cofor1)
        standard1.save()

        # workaround because of auto_now on created field
        RepackingStandard.objects.filter(SKU=sku1).update(created=time1)
        standard1.created = time1

        sku2 = 'b'
        cofor2 = 'a'
        time2 = datetime.datetime(2012, 12, 12)
        standard2 = RepackingStandard(SKU=sku2, COFOR=cofor2)
        standard2.save()

        # workaround because of auto_now on created field
        RepackingStandard.objects.filter(SKU=sku2).update(created=time2)
        standard2.created = time2

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({})
        self.assertEquals(repacking_standards[0], standard1)
        self.assertEquals(repacking_standards[1], standard2)
        self.assertEquals(len(repacking_standards), 2)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'order_by': 'SKU'})
        self.assertEquals(repacking_standards[0], standard1)
        self.assertEquals(repacking_standards[1], standard2)
        self.assertEquals(len(repacking_standards), 2)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'order_by': 'COFOR'})
        self.assertEquals(repacking_standards[0], standard2)
        self.assertEquals(repacking_standards[1], standard1)
        self.assertEquals(len(repacking_standards), 2)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get(
            {'order_by': 'takyto_field_neexistuje'})

        self.assertEquals(repacking_standards[0], standard1)
        self.assertEquals(repacking_standards[1], standard2)
        self.assertEquals(len(repacking_standards), 2)

    def test_order_reverse_repacking_standard(self):
        sku1 = "a"
        cofor1 = "b"
        standard1 = RepackingStandard(SKU=sku1, COFOR=cofor1)
        standard1.save()

        sku2 = 'b'
        cofor2 = 'a'
        standard2 = RepackingStandard(SKU=sku2, COFOR=cofor2)
        standard2.save()

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'order_by': '-SKU'})
        self.assertEquals(repacking_standards[0], standard2)
        self.assertEquals(repacking_standards[1], standard1)
        self.assertEquals(len(repacking_standards), 2)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'order_by': '-COFOR'})
        self.assertEquals(repacking_standards[0], standard1)
        self.assertEquals(repacking_standards[1], standard2)
        self.assertEquals(len(repacking_standards), 2)

    def test_filter_repacking_standard(self):
        sku1 = "abcd"
        cofor1 = "efgh"
        standard1 = RepackingStandard(SKU=sku1, COFOR=cofor1)
        standard1.save()
        sku2 = 'bcde'
        cofor2 = 'afgh'
        standard2 = RepackingStandard(SKU=sku2, COFOR=cofor2)
        standard2.save()

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'SKU': 'a'})
        self.assertEquals(repacking_standards[0], standard1)
        self.assertEquals(len(repacking_standards), 1)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'SKU': 'bcd'})
        self.assertEquals(len(repacking_standards), 2)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'COFOR': 'ef'})
        self.assertEquals(repacking_standards[0], standard1)
        self.assertEquals(len(repacking_standards), 1)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'COFOR': 'bla-bla'})
        self.assertEquals(len(repacking_standards), 0)

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({'nepodstany': 'zaznam'})
        self.assertEquals(len(repacking_standards), 2)

    def test_order_repacking_history(self):
        sku1 = "a"
        cofor1 = "b"
        time1 = datetime.datetime(2014, 10, 10)
        standard1 = RepackingStandard(SKU=sku1, COFOR=cofor1)
        standard1.save()
        repack1 = RepackHistory(repacking_standard=standard1, repack_start=time1, repack_finish=time1)
        repack1.save()

        sku2 = 'b'
        cofor2 = 'a'
        time2 = datetime.datetime(2012, 12, 12)
        standard2 = RepackingStandard(SKU=sku2, COFOR=cofor2)
        standard2.save()
        repack2 = RepackHistory(repacking_standard=standard2, repack_start=time2, repack_finish=time1)
        repack2.save()

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({})
        self.assertEquals(repacking_history[0], repack1)
        self.assertEquals(repacking_history[1], repack2)
        self.assertEquals(len(repacking_history), 2)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'order_by': 'repack_start'})
        self.assertEquals(repacking_history[0], repack2)
        self.assertEquals(repacking_history[1], repack1)
        self.assertEquals(len(repacking_history), 2)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'order_by': '-repack_start'})
        self.assertEquals(repacking_history[0], repack1)
        self.assertEquals(repacking_history[1], repack2)
        self.assertEquals(len(repacking_history), 2)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get(
            {'order_by': 'takyto_field_neexistuje'})

        self.assertEquals(repacking_history[0], repack1)
        self.assertEquals(repacking_history[1], repack2)
        self.assertEquals(len(repacking_history), 2)

    def test_filter_repacking_history(self):
        sku1 = "abcd"
        cofor1 = "efgh"
        time1 = datetime.datetime(2014, 12, 12)
        standard1 = RepackingStandard(SKU=sku1, COFOR=cofor1)
        standard1.save()
        repack1 = RepackHistory(repacking_standard=standard1, repack_start=time1, repack_finish=time1, idp="ababa")
        repack1.save()

        sku2 = 'bcde'
        cofor2 = 'afgh'
        time2 = datetime.datetime(2012, 12, 12)
        standard2 = RepackingStandard(SKU=sku2, COFOR=cofor2)
        standard2.save()
        repack2 = RepackHistory(repacking_standard=standard2, repack_start=time2, repack_finish=time1, idp="bebe")
        repack2.save()

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'repacking_standard__SKU': 'bcde'})
        self.assertEquals(repacking_history[0], repack2)
        self.assertEquals(len(repacking_history), 1)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'repacking_standard__SKU': 'bcd'})
        self.assertEquals(len(repacking_history), 2)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'repacking_standard__COFOR': 'ef'})
        self.assertEquals(repacking_history[0], repack1)
        self.assertEquals(len(repacking_history), 1)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'repacking_standard__COFOR': 'tis'})
        self.assertEquals(len(repacking_history), 0)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'repacking_standard__mmm': 'zaznam'})
        self.assertEquals(len(repacking_history), 2)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'idp': 'b'})
        self.assertEquals(len(repacking_history), 2)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'idp': 'ba'})
        self.assertEquals(repacking_history[0], repack1)
        self.assertEquals(len(repacking_history), 1)

        repacking_history = RepackHistory.filter_and_order_repacking_history_by_get({'idp': 'wpoegj'})
        self.assertEquals(len(repacking_history), 0)
