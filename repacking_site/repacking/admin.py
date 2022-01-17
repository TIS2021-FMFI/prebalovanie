from django.contrib import admin

from .models import *


class RepackingStandardAdmin(admin.ModelAdmin):
    list_display = (str, 'SKU', 'COFOR', 'destination', 'supplier')


admin.site.register(RepackingStandard, RepackingStandardAdmin)


class RepackingHistoryAdmin(admin.ModelAdmin):
    list_display = (str, 'repack_start', 'repack_finish', 'repack_duration', 'idp', 'repacking_standard')


admin.site.register(RepackHistory, RepackingHistoryAdmin)

admin.site.register(Tools)

admin.site.register(Photos)
