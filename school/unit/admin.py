from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from school.unit import models


class BaseAdmin(admin.ModelAdmin):
    search_fields = ('pk',)
    readonly_fields = ('pk',)


class StudentAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'number', 'class_room')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Teacher, UserAdmin)
admin.site.register(models.ClassRoom, BaseAdmin)
admin.site.register(models.ClassHomeWork, BaseAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Notification, BaseAdmin)
