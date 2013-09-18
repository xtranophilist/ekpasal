from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from users.forms import UserAdminForm

from models import User


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm


admin.site.register(User, UserAdmin)
admin.site.unregister(Site)

admin.site.unregister(Group)
admin.site.register(Group)
