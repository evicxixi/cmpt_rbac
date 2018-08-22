from django.contrib import admin

# Register your models here.
from rbac import models


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_menu', 'icon']
    list_editable = ['is_menu', 'url', 'icon']


admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(models.UserInfo)
# admin.site.register(models.)
# admin.site.register(models.)
# admin.site.register(models.)
# admin.site.register(models.)
