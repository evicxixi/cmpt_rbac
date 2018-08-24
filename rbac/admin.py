from django.contrib import admin

# Register your models here.
from rbac import models


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'name', 'parent', 'menu']
    list_editable = ['url', 'name', 'parent', 'menu']


admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(models.UserInfo)
admin.site.register(models.Menu)
# admin.site.register(models.)
# admin.site.register(models.)
# admin.site.register(models.)
