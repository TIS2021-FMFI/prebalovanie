from django.db import models
import datetime


class RepackingStandard(models.Model):
	SKU_code = models.CharField(max_length=50, default="", unique=True)
	COFOR_code = models.CharField(max_length=50, default="")
	supplier = models.CharField(max_length=50, default="")
	destination = models.CharField(max_length=50, default="")
	pcs_per_move = models.IntegerField(default=0)
	datetime_of_create = models.DateTimeField(auto_now=True)
	unit_weight = models.DecimalField(max_digits=6, decimal_places=4, default=0)
	repacking_time = models.DurationField(default=datetime.timedelta(minutes=0))
	remark = models.CharField(max_length=1200, default="")

	pcs_package_in = models.IntegerField(default=0)
	pcs_package_out = models.IntegerField(default=0)

	boxes_on_pallet_in = models.IntegerField(default=0)
	boxes_on_pallet_out = models.IntegerField(default=0)

	pcs_on_pallet_in = models.IntegerField(default=0)
	pcs_on_pallet_out = models.IntegerField(default=0)

	package_type_in = models.CharField(max_length=50, default="")
	package_type_out = models.CharField(max_length=50, default="")

	def __str__(self):
		return str(self.SKU_code)+"\t"+str(self.COFOR_code)

	@staticmethod
	def get_repacking_standard_by_sku(sku_code):
		try:
			standard = RepackingStandard.objects.get(SKU_code=sku_code)
			return standard
		except RepackingStandard.DoesNotExist:
			return None


class Repack(models.Model):
	repacking_standard = models.ForeignKey(RepackingStandard, on_delete=models.SET_NULL, null=True)
	repack_datetime = models.DateTimeField(auto_now=True)
	idp = models.CharField(max_length=50)


