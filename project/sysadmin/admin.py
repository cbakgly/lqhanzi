from django.contrib import admin

# Register your models here.
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from sysadmin.models import User
from django.contrib.auth.models import Permission


admin.site.register(User, GuardedModelAdmin)
admin.site.register(Permission, GuardedModelAdmin)