from django.test import TestCase

from .models import RepackingStandard


class RepackingStandardsModelTests(TestCase):

    def test_dummy(self):
        self.assertIs(True, True)

    def test_get_repacking_standard_by_sku(self):
        sku = "sku"
        cofor = "cofor"
        standard = RepackingStandard(SKU_code=sku, COFOR_code=cofor)
        standard.save()
        for i in range(10):
            RepackingStandard(SKU_code=sku+str(i), COFOR_code=cofor).save()

        self.assertEqual(standard.SKU_code, RepackingStandard.get_repacking_standard_by_sku(sku).SKU_code)
        self.assertEqual(sku, RepackingStandard.get_repacking_standard_by_sku(sku).SKU_code)

        self.assertEqual(cofor, RepackingStandard.get_repacking_standard_by_sku(sku).COFOR_code)

        self.assertNotEqual(standard.SKU_code, RepackingStandard.get_repacking_standard_by_sku(sku+str(1)).SKU_code)
