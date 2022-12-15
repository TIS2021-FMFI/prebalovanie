from django.db import models
from datetime import *
from django.conf import settings

from accounts.models import *


class Tools(models.Model):
    class Meta:
        verbose_name = 'OPP'
        verbose_name_plural = 'OPP'
        permissions = ()
        default_permissions = ()

    def __str__(self):
        return f'OPP {str(self.id)}'

    photo = models.ImageField(upload_to='tools/%Y/%m/')


class Photos(models.Model):
    class Meta:
        verbose_name = 'Fotka'
        verbose_name_plural = 'Fotky'
        permissions = ()
        default_permissions = ()

    def __str__(self):
        return f'Fotka {str(self.id)}'

    photo = models.ImageField(upload_to='photos/%Y/%m/')


class RepackingStandard(models.Model):
    class Meta:
        verbose_name = 'Štandard'
        verbose_name_plural = 'Štandardy'
        permissions = ()
        default_permissions = ()

    SKU = models.CharField(max_length=50, default="", unique=True, verbose_name="SKU")
    COFOR = models.CharField(max_length=50, default="", verbose_name="COFOR")
    supplier = models.CharField(max_length=50, default="", verbose_name="Dodávateľ")
    destination = models.CharField(max_length=50, default="", verbose_name="Destinácia")
    items_per_move = models.PositiveIntegerField(default=0, verbose_name="kusov na pohyb")
    unit_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Jednotková váha")
    repacking_duration = models.DurationField(default=timedelta(minutes=0), verbose_name="Doba prebalu")
    instructions = models.CharField(max_length=1200, default="", verbose_name="Inštrukcie")
    tools = models.ManyToManyField(Tools, related_name='tools', blank=True, verbose_name="OPP")

    input_count_of_items_in_package = models.PositiveIntegerField(default=0, verbose_name="KS vo vstupnom balení")
    output_count_of_items_in_package = models.PositiveIntegerField(default=0, verbose_name="KS vo výstupnom balení")

    input_count_of_boxes_on_pallet = models.PositiveIntegerField(default=0, verbose_name="Boxov na vstupnej palete")
    output_count_of_boxes_on_pallet = models.PositiveIntegerField(default=0, verbose_name="Boxov na výstupnej palete")

    input_count_of_items_on_pallet = models.PositiveIntegerField(default=0, verbose_name="KS na vstupnej palete")
    output_count_of_items_on_pallet = models.PositiveIntegerField(default=0, verbose_name="KS na výstupnej palete")

    input_type_of_package = models.CharField(max_length=50, default="", verbose_name="Druh vstupného obalu")
    output_type_of_package = models.CharField(max_length=50, default="", verbose_name="Druh výstupného obalu")

    input_photos = models.ManyToManyField(Photos, related_name='input_photos',
                                          blank=True, verbose_name="Fotky vstupného obalu")
    output_photos = models.ManyToManyField(Photos, related_name='output_photos',
                                           blank=True, verbose_name="Fotky výstupného obalu")

    created = models.DateTimeField(auto_now=True, verbose_name="Čas vytvorenia")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, related_name='creator', verbose_name="Vytvoril používateľ")

    def __str__(self):
        return f'Štandard {str(self.id)}'

    @staticmethod
    def get_standard(sku_code, destination):
        try:
            standard = RepackingStandard.objects.get(SKU=sku_code, destination=destination)
            return standard
        except RepackingStandard.DoesNotExist:
            return None

    @staticmethod
    def filter_and_order_repacking_standard_by_get(get):
        order_by = get.get('order_by', "-created")
        try:
            if order_by[0] == '-':
                RepackingStandard._meta.get_field(order_by[1:])
            else:
                RepackingStandard._meta.get_field(order_by)
        except:
            order_by = "-created"
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
    class Meta:
        verbose_name = 'Prebaľovanie'
        verbose_name_plural = 'Prebaľovania'
        permissions = ()
        default_permissions = ()

    repacking_standard = models.ForeignKey(RepackingStandard, on_delete=models.SET_NULL, null=True,
                                           related_name='repacking_standard', verbose_name="Štandard")
    repack_start = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Začiatok prebalu")
    repack_finish = models.DateTimeField(auto_now=False, verbose_name="Konies prebalu")
    repack_duration = models.DurationField(default=timedelta(minutes=0), verbose_name="Trvanie prebalu")
    idp = models.CharField(max_length=50, verbose_name="IDP")
    users = models.ManyToManyField(User, related_name='users', verbose_name="Prebaľovali používatelia")

    def repack_duration_str(self):
        sec = self.repack_duration.total_seconds()
        return '%02d:%02d:%02d' % (int((sec / 3600) % 3600), int((sec / 60) % 60), int(sec % 60))

    def __str__(self):
        return f'Prebaľovanie {str(self.id)}'

    @staticmethod
    def filter_and_order_repacking_history_by_get(get):
        order_by = get.get('order_by', "-repack_start")
        try:
            if order_by[0] == '-':
                RepackHistory._meta.get_field(order_by[1:])
            else:
                RepackHistory._meta.get_field(order_by)
        except:
            order_by = "-repack_start"
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

    @staticmethod
    def write_repacking_history_to_csv(repacks, writer):
        writer.writerow(['Čas začiatku prebalu', 'Čas konca prebalu', 'Čas prebalu', 'operátori',
                         'SKU', 'COFOR', 'Destinácia', 'ks IN', 'ks OUT',
                         'ks v obale IN', 'ks v obale OUT', 'boxy IN', 'boxy OUT',
                         'Trvanie prebalu podľa štandardu', 'kg/ks', 'vytvoril', 'Čas vytvorenia', 'Poznámka'])

        for repack in repacks:
            writer.writerow([repack.repack_start, repack.repack_finish, repack.repack_duration,
                             ', '.join(map(str, repack.users.all())),
                             repack.repacking_standard.SKU, repack.repacking_standard.COFOR,
                             repack.repacking_standard.destination,
                             repack.repacking_standard.input_count_of_items_on_pallet,
                             repack.repacking_standard.output_count_of_items_on_pallet,
                             repack.repacking_standard.input_count_of_items_in_package,
                             repack.repacking_standard.output_count_of_items_in_package,
                             repack.repacking_standard.input_count_of_boxes_on_pallet,
                             repack.repacking_standard.output_count_of_boxes_on_pallet,
                             repack.repacking_standard.repacking_duration,
                             repack.repacking_standard.unit_weight, repack.repacking_standard.creator,
                             repack.repacking_standard.created, repack.repacking_standard.instructions])
