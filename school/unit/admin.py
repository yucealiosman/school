from django.contrib import admin

from school.unit import models


class BaseAdmin(admin.ModelAdmin):
    search_fields = ('pk',)
    readonly_fields = ('pk',)


admin.site.register(models.Student, BaseAdmin)
admin.site.register(models.Teacher, BaseAdmin)
admin.site.register(models.ClassRoom, BaseAdmin)
admin.site.register(models.ClassHomeWork, BaseAdmin)
