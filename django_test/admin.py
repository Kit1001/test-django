from django.contrib import admin

from .models import *


# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    pass


class MenuItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)
