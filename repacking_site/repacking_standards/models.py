from django.db import models

class repacking_standard(models.Model):
	SKU_code = models.CharField(max_length=50)
	COFOR_code = models.CharField(max_length=50)
	datetime_of_create = models.DateTimeField(auto_now=True)
	unit_weight = models.DecimalField(max_digits=6, decimal_places=2)
