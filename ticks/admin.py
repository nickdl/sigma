from django.contrib import admin
from ticks.models import Tick


@admin.register(Tick)
class TickAdmin(admin.ModelAdmin):
    list_display = ('date', 'symbol', 'close', 'volume')
