from django.db import models
from datetime import *
from django.conf import settings

from accounts.models import *


class Tools(models.Model):
    photo = models.ImageField(upload_to='tools/%Y/%m/')


class Photos(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/')


class RepackingStandard(models.Model):
    SKU = models.CharField(max_length=50, default="", unique=True)
    COFOR = models.CharField(max_length=50, default="")
    supplier = models.CharField(max_length=50, default="")
    destination = models.CharField(max_length=50, default="")
    items_per_move = models.PositiveIntegerField(default=0)
    unit_weight = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    repacking_duration = models.DurationField(default=timedelta(minutes=0))
    instructions = models.CharField(max_length=1200, default="")
    tools = models.ManyToManyField(Tools, related_name='tools', blank=True)

    input_count_of_items_in_package = models.PositiveIntegerField(default=0)
    output_count_of_items_in_package = models.PositiveIntegerField(default=0)

    input_count_of_boxes_on_pallet = models.PositiveIntegerField(default=0)
    output_count_of_boxes_on_pallet = models.PositiveIntegerField(default=0)

    input_count_of_items_on_pallet = models.PositiveIntegerField(default=0)
    output_count_of_items_on_pallet = models.PositiveIntegerField(default=0)

    input_type_of_package = models.CharField(max_length=50, default="")
    output_type_of_package = models.CharField(max_length=50, default="")

    input_photos = models.ManyToManyField(Photos, related_name='input_photos', blank=True)
    output_photos = models.ManyToManyField(Photos, related_name='output_photos', blank=True)

    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='creator')

    def __str__(self):
        return f'sku: {str(self.SKU)} cofor:{str(self.COFOR)}'

    @staticmethod
    def get_repacking_standard_by_sku(sku_code):
        try:
            standard = RepackingStandard.objects.get(SKU=sku_code)
            return standard
        except RepackingStandard.DoesNotExist:
            return None

    @staticmethod
    def filter_and_order_repacking_standard_by_get(get):
        order_by = get.get('order_by', "created")
        try:
            if order_by[0] == '-':
                RepackingStandard._meta.get_field(order_by[1:])
            else:
                RepackingStandard._meta.get_field(order_by)
        except:
            order_by = "created"
        repacking_standards = RepackingStandard.objects.filter(
            SKU__contains=get.get('SKU', ""),
            COFOR__contains=get.get('COFOR', ""),
            supplier__contains=get.get('supplier', ""),
            destination__contains=get.get('destination', ""),
            input_type_of_package__contains=get.get('input_type_of_package', ""),
            output_type_of_package__contains=get.get('output_type_of_package', "")
        ).order_by(order_by)
        return repacking_standards


class RepackHistory(models.Model):
    repacking_standard = models.ForeignKey(RepackingStandard,
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           related_name='repacking_standard')
    repack_start = models.DateTimeField(default=datetime.now, blank=True)
    repack_finish = models.DateTimeField(auto_now=False)
    repack_duration = models.DurationField(default=timedelta(minutes=0))
    idp = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='users')

    def __str__(self):
        return f'standard: sku:{str(self.repacking_standard)}, cofor:{str(self.repack_start)}'

    @staticmethod
    def filter_and_order_repacking_history_by_get(get):
        order_by = get.get('order_by', "repack_start")
        try:
            if order_by[0] == '-':
                RepackHistory._meta.get_field(order_by[1:])
            else:
                RepackHistory._meta.get_field(order_by)
        except:
            order_by = "repack_start"
        repacking_history = RepackHistory.objects.filter(
            idp__contains=get.get('idp', ""),
            repacking_standard__SKU__contains=get.get('repacking_standard__SKU', ""),
            repacking_standard__COFOR__contains=get.get('repacking_standard__COFOR', ""),
            repacking_standard__supplier__contains=get.get('repacking_standard__supplier', ""),
            repacking_standard__destination__contains=get.get('repacking_standard__destination', ""),
            repacking_standard__input_type_of_package__contains=get.get('repacking_standard__input_type_of_package',
                                                                        ""),
            repacking_standard__output_type_of_package__contains=get.get('repacking_standard__output_type_of_package',
                                                                         "")
        ).order_by(order_by)
        return repacking_history
