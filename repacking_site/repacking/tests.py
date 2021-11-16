from django.test import TestCase

from .models import RepackingStandard


class RepackingStandardsModelTests(TestCase):

    def test_dummy(self):
        self.assertIs(True, True)

    def test_get_repacking_standard_by_sku(self):
        sku = "sku"
        cofor = "cofor"
        standard = RepackingStandard(SKU=sku, COFOR=cofor)
        standard.save()
        for i in range(10):
            RepackingStandard(SKU=sku+str(i), COFOR=cofor).save()

        self.assertEqual(standard.SKU, RepackingStandard.get_repacking_standard_by_sku(sku).SKU)
        self.assertEqual(sku, RepackingStandard.get_repacking_standard_by_sku(sku).SKU)

        self.assertEqual(cofor, RepackingStandard.get_repacking_standard_by_sku(sku).COFOR)

        self.assertNotEqual(standard.SKU, RepackingStandard.get_repacking_standard_by_sku(sku + str(1)).SKU)
