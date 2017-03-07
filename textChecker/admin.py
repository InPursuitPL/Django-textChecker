from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import StringText, PersonalData

admin.site.register(StringText)


class PersonalDataInline(admin.StackedInline):
    model = PersonalData
    can_delete = False
    verbose_name_plural = 'Personal Data'


class UserAdmin(BaseUserAdmin):
    inlines = (PersonalDataInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


