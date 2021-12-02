from django.test import TestCase

from .models import RepackingStandard
import datetime


class RepackingStandardsModelTests(TestCase):

    def test_dummy(self):
        self.assertIs(True, True)

    def test_get_repacking_standard_by_sku(self):
        sku = "sku"
        cofor = "cofor"
        standard = RepackingStandard(SKU=sku, COFOR=cofor)
        standard.save()
        for i in range(10):
            RepackingStandard(SKU=sku + str(i), COFOR=cofor).save()

        self.assertEqual(standard.SKU, RepackingStandard.get_repacking_standard_by_sku(sku).SKU)
        self.assertEqual(sku, RepackingStandard.get_repacking_standard_by_sku(sku).SKU)

        self.assertEqual(cofor, RepackingStandard.get_repacking_standard_by_sku(sku).COFOR)

        self.assertNotEqual(standard.SKU, RepackingStandard.get_repacking_standard_by_sku(sku + str(1)).SKU)

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
        standard1.created = time2

        repacking_standards = RepackingStandard.filter_and_order_repacking_standard_by_get({})

        self.assertEquals(repacking_standards[0], standard2)
        self.assertEquals(repacking_standards[1], standard1)
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

        self.assertEquals(repacking_standards[0], standard2)
        self.assertEquals(repacking_standards[1], standard1)
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
